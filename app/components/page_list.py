"""Shared sortable/filterable page list component."""

from __future__ import annotations

from nicegui import ui

from app.components.badges import type_badge
from app.wiki import WikiPage, WikiStore

SORT_OPTIONS = {
    "name": "Name",
    "backlinks": "In-links",
    "outlinks": "Out-links",
    "total_links": "Total links",
}

SORT_KEYS = {
    "name": lambda p: p._title_lower,
    "backlinks": lambda p: (-len(p.backlinks), p._title_lower),
    "outlinks": lambda p: (-len(p.outlinks), p._title_lower),
    "total_links": lambda p: (-(len(p.backlinks) + len(p.outlinks)), p._title_lower),
}


def page_list_controls(
    pages: list[WikiPage],
    store: WikiStore,
    *,
    show_type_badge: bool = True,
) -> None:
    """Render a page list with sort and tag filter controls."""
    sort_value = {"current": "name"}
    tag_value = {"current": ""}

    list_container = ui.column().classes("w-full gap-2")

    def render_list() -> None:
        list_container.clear()
        filtered = pages
        if tag_value["current"]:
            filtered = [p for p in filtered if tag_value["current"] in p.tags]

        key_fn = SORT_KEYS.get(sort_value["current"], SORT_KEYS["name"])
        sorted_pages = sorted(filtered, key=key_fn)

        with list_container:
            if not sorted_pages:
                ui.label("No pages match the selected filter.").style(
                    "color: var(--text-muted)"
                )
                return
            ui.label(f"{len(sorted_pages)} pages").style(
                "color: var(--text-muted); font-size: 0.875rem"
            )
            for page in sorted_pages:
                with ui.link(target=page.url).classes("no-underline w-full"):
                    with ui.row().classes(
                        "w-full items-center gap-3 px-4 py-2 rounded-lg theme-hover"
                    ).style("transition: background-color 0.15s"):
                        if show_type_badge:
                            type_badge(page.type)
                        ui.label(page.title).style(
                            "color: var(--text-primary); font-size: 0.875rem"
                        )
                        ui.space()
                        if page.tags:
                            for tag in page.tags[:2]:
                                ui.badge(tag).classes(
                                    "text-xs"
                                ).style(
                                    "background-color: var(--bg-secondary); "
                                    "color: var(--text-secondary); "
                                    "border: 1px solid var(--border)"
                                )
                        ui.label(
                            f"{len(page.backlinks)}in {len(page.outlinks)}out"
                        ).style("color: var(--text-muted); font-size: 0.75rem")

    def on_sort_change(e) -> None:
        sort_value["current"] = e.value
        render_list()

    def on_tag_change(e) -> None:
        tag_value["current"] = e.value or ""
        render_list()

    with ui.row().classes("w-full items-center gap-4 flex-wrap"):
        ui.select(
            options=SORT_OPTIONS,
            value="name",
            label="Sort by",
            on_change=on_sort_change,
        ).classes("w-40").props("outlined dense dark")

        all_tags = store.get_all_tags()
        ui.select(
            options=[""] + all_tags,
            value="",
            label="Filter by tag",
            on_change=on_tag_change,
        ).classes("w-48").props("outlined dense dark clearable")

    render_list()
