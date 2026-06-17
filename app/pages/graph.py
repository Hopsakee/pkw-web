"""Graph view: community-clustered graph of the wiki.

Nodes are real wiki pages (the five folders); `index`/`wiki` and any link to a
non-existent page are excluded. Node size scales with the number of *backlinks*
(incoming links). Node colour comes from `TYPE_CONFIG` — the same per-type colours
the rest of the app uses. The ECharts legend toggles types on/off; a tag multi-select
filters to pages carrying the chosen tag(s).

Layout is precomputed server-side: Louvain community detection over the link
graph partitions pages into topical clusters, each cluster gets its own spring
layout dropped onto a well-separated slot of a ring (clusters never overlap), and
ECharts renders the fixed positions with `layout: 'none'` — fully automatic,
deterministic, instant, no force simulation.
"""

from __future__ import annotations

import math

import networkx as nx
from nicegui import events, ui

from app.components.layout import page_layout
from app.config import Settings
from app.wiki import TYPE_CONFIG, WikiStore

# Slugs that must never appear as nodes even if something links to them.
_EXCLUDE_SLUGS = {"index", "wiki", "WIKI", "help"}

# Fallback colour for a page whose `type:` is not one of the five known types.
_FALLBACK_COLOR = "#6b8aaa"


def _symbol_size(backlinks: int) -> float:
    """Node radius driven by incoming-link count. sqrt keeps hubs from dwarfing
    the rest; the +6 floor keeps zero-backlink nodes visible."""
    return round(6 + 5 * (backlinks ** 0.5), 1)


def _compute_positions(
    node_ids: set[str], edges: list[dict]
) -> dict[str, tuple[float, float]]:
    """Precompute a clustered, non-overlapping layout — fully automatic, no
    manual grouping. Louvain community detection over the link graph partitions
    pages into topical clusters. The clusters are packed into a square grid (one
    cell each, cell pitch sized to the biggest cluster) so they fill the plane
    evenly — close together, every cell used, no outlier flinging the view's
    extent. Each cluster's own members get a spring layout sized by node count,
    so dense clusters spread out instead of piling up. Singleton / unlinked pages
    are pooled into one extra cluster. Deterministic (fixed seeds) → identical
    every load."""
    graph = nx.Graph()
    graph.add_nodes_from(node_ids)
    graph.add_edges_from((e["source"], e["target"]) for e in edges)

    communities = nx.community.louvain_communities(graph, seed=42)
    multi = sorted((c for c in communities if len(c) >= 2), key=len, reverse=True)
    singles = {n for c in communities if len(c) == 1 for n in c}
    clusters: list[set[str]] = [set(c) for c in multi] + (
        [singles] if singles else []
    )
    n = len(clusters)
    if n == 0:
        return {s: (0.0, 0.0) for s in node_ids}

    # A cluster's radius scales with sqrt(node count) so its *area* tracks its
    # size — only ratios matter (ECharts auto-fits the extent to the viewport).
    radii = [math.sqrt(len(c)) for c in clusters]

    if n == 1:
        local = nx.spring_layout(graph, seed=42, scale=radii[0])
        return {s: (round(x, 1), round(y, 1)) for s, (x, y) in local.items()}

    # ---- level 1: pack clusters into a square grid (uniform fill, no outliers) -
    cols = math.ceil(math.sqrt(n))
    # cell pitch: biggest cluster's diameter plus a small breathing margin, so
    # adjacent cells sit close but the largest cluster still never spills over.
    pitch = 2 * max(radii) + 0.35 * max(radii)

    # ---- level 2: drop each cluster's members around its grid-cell centre ------
    pos: dict[str, tuple[float, float]] = {}
    for i, members in enumerate(clusters):
        cx = (i % cols) * pitch
        cy = (i // cols) * pitch
        local = nx.spring_layout(graph.subgraph(members), seed=42, scale=radii[i])
        for slug, (lx, ly) in local.items():
            pos[slug] = (round(cx + lx, 1), round(cy + ly, 1))
    for slug in node_ids:  # safety: anything the layout missed → origin
        pos.setdefault(slug, (0.0, 0.0))
    return pos


def register(store: WikiStore, settings: Settings) -> None:
    # ---- precompute the full graph once (cheap; data is already in memory) ----
    types = list(TYPE_CONFIG.keys())
    type_index = {t: i for i, t in enumerate(types)}
    categories = [
        {"name": t, "itemStyle": {"color": TYPE_CONFIG[t]["color"]}}
        for t in types
    ]

    nodes_all: list[dict] = []
    node_slugs: set[str] = set()
    for page in store.get_all_pages():
        if page.slug in _EXCLUDE_SLUGS:
            continue
        cat = type_index.get(page.type)
        node = {
            "id": page.slug,
            "name": page.title,
            "symbolSize": _symbol_size(len(page.backlinks)),
            "value": len(page.backlinks),
            "tags": [str(t) for t in page.tags],
            "url": page.url,
        }
        if cat is not None:
            node["category"] = cat
        else:
            node["itemStyle"] = {"color": _FALLBACK_COLOR}
        nodes_all.append(node)
        node_slugs.add(page.slug)

    # Edges: outlinks that resolve to a real, included node. Directed, de-duped,
    # no self-loops. Dangling links (to unmaterialised pages) are dropped.
    edge_set: set[tuple[str, str]] = set()
    for page in store.get_all_pages():
        if page.slug not in node_slugs:
            continue
        for target in page.outlinks:
            if target in node_slugs and target != page.slug:
                edge_set.add((page.slug, target))
    edges_all = [{"source": s, "target": t} for s, t in sorted(edge_set)]

    # Precomputed clustered layout (Louvain) — give every node a fixed x/y.
    positions = _compute_positions(node_slugs, edges_all)
    for node in nodes_all:
        node["x"], node["y"] = positions[node["id"]]

    url_by_name = {n["name"]: n["url"] for n in nodes_all}

    def build_options(selected_tags: list[str]) -> dict:
        if selected_tags:
            wanted = set(selected_tags)
            nodes = [n for n in nodes_all if wanted.intersection(n["tags"])]
        else:
            nodes = nodes_all
        kept = {n["id"] for n in nodes}
        links = [e for e in edges_all if e["source"] in kept and e["target"] in kept]
        return {
            "tooltip": {"formatter": "{b} — {c} backlinks"},
            "legend": [{
                "data": types,
                "textStyle": {"color": "#a0b4c8"},
            }],
            "series": [{
                "type": "graph",
                # Positions are precomputed (Louvain clusters on a ring) and fixed
                # on each node's x/y — 'none' means ECharts draws them as-is, no
                # force sim. Deterministic, instant, and clusters never overlap.
                "layout": "none",
                "roam": True,
                "draggable": True,
                # Keep nodes/labels a constant screen size while zooming/roaming
                # (default 0.6 grows them with zoom). 0 = pan/zoom the canvas,
                # symbols stay put.
                "nodeScaleRatio": 0,
                "categories": categories,
                "data": nodes,
                "links": links,
                "label": {"show": False, "position": "right", "color": "#e8edf2"},
                "lineStyle": {"color": "source", "opacity": 0.35, "width": 0.8},
                "emphasis": {"focus": "adjacency", "label": {"show": True}},
            }],
        }

    @ui.page("/graph")
    def graph_page() -> None:
        with page_layout("Graph"):
            ui.label("Graph").style(
                "color: var(--text-primary); font-size: 1.875rem; font-weight: 700"
            )
            ui.label(
                f"{len(nodes_all)} pages · {len(edges_all)} links · "
                "node size = backlinks · click a type in the legend to toggle it"
            ).style("color: var(--text-muted); font-size: 0.875rem; margin-top: -1rem")

            with ui.row().classes("w-full items-center gap-3"):
                tag_select = ui.select(
                    options=store.get_all_tags(),
                    multiple=True,
                    label="Filter op tags",
                    with_input=True,
                ).props("outlined dense use-chips clearable").classes(
                    "sort-select min-w-[280px] flex-1"
                )

            chart = ui.echart(
                build_options([]),
                on_point_click=_on_node_click,
            ).classes("w-full").style(
                "height: 75vh; background-color: var(--bg-secondary);"
                " border: 1px solid var(--border); border-radius: 12px"
            )

            def apply_tag_filter() -> None:
                # EChart.options is read-only (no setter in NiceGUI 3.x) — mutate
                # the existing dict in place, then push with update().
                chart.options.clear()
                chart.options.update(build_options(list(tag_select.value or [])))
                chart.update()

            tag_select.on_value_change(apply_tag_filter)

    def _on_node_click(e: events.EChartPointClickEventArguments) -> None:
        # Only graph nodes carry a url; clicking an edge has no name match.
        url = None
        if isinstance(getattr(e, "data", None), dict):
            url = e.data.get("url")
        if not url:
            url = url_by_name.get(getattr(e, "name", None))
        if url:
            ui.navigate.to(url)
