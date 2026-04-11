"""Individual wiki page view: markdown content + backlinks/outlinks."""

from nicegui import ui

from app.components.badges import type_badge
from app.components.layout import page_layout
from app.components.markdown import render_wiki_markdown
from app.config import Settings
from app.wiki import WikiStore


def _sidebar_link(store: WikiStore, slug: str, show_broken: bool = False) -> None:
    """Render a resolved wiki link, or a broken fallback if show_broken is True."""
    resolved = store.resolve_slug(slug)
    if resolved:
        folder, _ = resolved
        linked = store.get_page(folder, slug)
        title = linked.title if linked else slug
        ui.link(title, f"/wiki/{folder}/{slug}").classes("sidebar-link block")
    elif show_broken:
        ui.label(slug.replace("-", " ").title()).classes(
            "text-slate-600 text-sm line-through"
        )


def _sidebar_section(
    label: str, slugs: list[str], store: WikiStore, *, show_broken: bool = False
) -> None:
    """Render a sidebar card with a list of wiki links."""
    if not slugs:
        return
    with ui.element("div").classes("wiki-card"):
        ui.label(f"{label} ({len(slugs)})").classes(
            "text-sm font-semibold text-slate-300 mb-2"
        )
        for slug in slugs:
            _sidebar_link(store, slug, show_broken=show_broken)


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/wiki/{folder}/{slug}")
    def wiki_page(folder: str, slug: str) -> None:
        page = store.get_page(folder, slug)

        if not page:
            with page_layout("Not Found"):
                ui.label(f"Page not found: {folder}/{slug}").classes("text-red-400")
            return

        with page_layout(page.title):
            with ui.row().classes("items-center gap-3 flex-wrap"):
                type_badge(page.type)
                ui.label(page.title).classes("text-2xl font-bold text-slate-100")

            with ui.row().classes("gap-4 flex-wrap -mt-2"):
                if page.created:
                    ui.label(f"Created: {page.created}").classes("text-slate-500 text-xs")
                if page.updated:
                    ui.label(f"Updated: {page.updated}").classes("text-slate-500 text-xs")
                if page.tags:
                    for tag in page.tags:
                        ui.badge(tag).classes("text-xs bg-slate-700 text-slate-300")

            with ui.row().classes("w-full gap-6 items-start"):
                with ui.column().classes("flex-1 min-w-0"):
                    html = render_wiki_markdown(page.content, store)
                    ui.html(html).classes("wiki-content")

                with ui.column().classes("w-64 shrink-0 gap-4"):
                    _sidebar_section("Backlinks", sorted(page.backlinks), store)
                    _sidebar_section(
                        "Outlinks", sorted(set(page.outlinks)), store, show_broken=True
                    )
                    _sidebar_section("Sources", page.sources, store, show_broken=True)
