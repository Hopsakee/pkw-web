"""Individual wiki page view: markdown content + backlinks/outlinks."""

from nicegui import ui

from app.components.badges import type_badge
from app.components.layout import page_layout
from app.components.markdown import render_wiki_markdown
from app.config import Settings
from app.wiki import WikiStore


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/wiki/{folder}/{slug}")
    def wiki_page(folder: str, slug: str) -> None:
        page = store.get_page(folder, slug)

        if not page:
            with page_layout("Not Found"):
                ui.label(f"Page not found: {folder}/{slug}").classes("text-red-400")
            return

        with page_layout(page.title):
            # Page header
            with ui.row().classes("items-center gap-3 flex-wrap"):
                type_badge(page.type)
                ui.label(page.title).classes("text-2xl font-bold text-slate-100")

            # Metadata row
            with ui.row().classes("gap-4 flex-wrap -mt-2"):
                if page.created:
                    ui.label(f"Created: {page.created}").classes("text-slate-500 text-xs")
                if page.updated:
                    ui.label(f"Updated: {page.updated}").classes("text-slate-500 text-xs")
                if page.tags:
                    for tag in page.tags:
                        ui.badge(tag).classes("text-xs bg-slate-700 text-slate-300")

            # Main content + sidebar
            with ui.row().classes("w-full gap-6 items-start"):
                # Content
                with ui.column().classes("flex-1 min-w-0"):
                    html = render_wiki_markdown(page.content, store)
                    ui.html(html).classes("wiki-content")

                # Sidebar
                with ui.column().classes("w-64 shrink-0 gap-4"):
                    # Backlinks
                    if page.backlinks:
                        with ui.element("div").classes("wiki-card"):
                            ui.label(f"Backlinks ({len(page.backlinks)})").classes(
                                "text-sm font-semibold text-slate-300 mb-2"
                            )
                            for bl_slug in sorted(page.backlinks):
                                resolved = store.resolve_slug(bl_slug)
                                if resolved:
                                    bl_folder, _ = resolved
                                    bl_page = store.get_page(bl_folder, bl_slug)
                                    title = bl_page.title if bl_page else bl_slug
                                    ui.link(title, f"/wiki/{bl_folder}/{bl_slug}").classes(
                                        "sidebar-link block"
                                    )

                    # Outlinks
                    if page.outlinks:
                        with ui.element("div").classes("wiki-card"):
                            ui.label(f"Outlinks ({len(page.outlinks)})").classes(
                                "text-sm font-semibold text-slate-300 mb-2"
                            )
                            for ol_slug in sorted(set(page.outlinks)):
                                resolved = store.resolve_slug(ol_slug)
                                if resolved:
                                    ol_folder, _ = resolved
                                    ol_page = store.get_page(ol_folder, ol_slug)
                                    title = ol_page.title if ol_page else ol_slug
                                    ui.link(title, f"/wiki/{ol_folder}/{ol_slug}").classes(
                                        "sidebar-link block"
                                    )
                                else:
                                    ui.label(ol_slug.replace("-", " ").title()).classes(
                                        "text-slate-600 text-sm line-through"
                                    )

                    # Sources
                    if page.sources:
                        with ui.element("div").classes("wiki-card"):
                            ui.label(f"Sources ({len(page.sources)})").classes(
                                "text-sm font-semibold text-slate-300 mb-2"
                            )
                            for src_slug in page.sources:
                                resolved = store.resolve_slug(src_slug)
                                if resolved:
                                    src_folder, _ = resolved
                                    src_page = store.get_page(src_folder, src_slug)
                                    title = src_page.title if src_page else src_slug
                                    ui.link(title, f"/wiki/{src_folder}/{src_slug}").classes(
                                        "sidebar-link block"
                                    )
                                else:
                                    ui.label(src_slug.replace("-", " ")).classes(
                                        "text-slate-500 text-sm"
                                    )
