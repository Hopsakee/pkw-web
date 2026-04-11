"""Home page: stats dashboard + folder cards + recent pages."""

from nicegui import ui

from app.components.badges import type_badge
from app.components.layout import page_layout
from app.config import Settings
from app.wiki import FOLDER_TO_TYPE, TYPE_CONFIG, WIKI_FOLDERS, WikiStore


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/")
    def home_page() -> None:
        with page_layout("Home"):
            stats = store.get_stats()

            # Hero
            ui.label("Personal Knowledge Wiki").classes(
                "text-3xl font-bold text-slate-100"
            )
            ui.label(
                f"{stats.total_pages} pages \u00b7 {stats.total_links} cross-references"
            ).classes("text-slate-400 text-sm -mt-4")

            # Stats row
            with ui.row().classes("w-full gap-4 flex-wrap"):
                for label, count, color in [
                    ("Entities", stats.entities, TYPE_CONFIG["entity"]["color"]),
                    ("Concepts", stats.concepts, TYPE_CONFIG["concept"]["color"]),
                    ("Sources", stats.sources, TYPE_CONFIG["source"]["color"]),
                    ("Comparisons", stats.comparisons, TYPE_CONFIG["comparison"]["color"]),
                    ("Syntheses", stats.syntheses, TYPE_CONFIG["synthesis"]["color"]),
                ]:
                    with ui.element("div").classes("stat-card flex-1 min-w-[140px]"):
                        ui.label(str(count)).classes("text-2xl font-bold").style(f"color: {color}")
                        ui.label(label).classes("text-slate-400 text-xs mt-1")

            # Folder cards
            ui.label("Browse by Type").classes("text-lg font-semibold text-slate-200 mt-4")
            with ui.row().classes("w-full gap-4 flex-wrap"):
                for folder in WIKI_FOLDERS:
                    wiki_type = FOLDER_TO_TYPE[folder]
                    cfg = TYPE_CONFIG.get(wiki_type, {})
                    count = stats.counts.get(folder, 0)
                    with ui.link(target=f"/wiki/{folder}").classes("no-underline flex-1 min-w-[180px]"):
                        with ui.element("div").classes("wiki-card cursor-pointer"):
                            ui.label(f"{cfg.get('icon', '')} {folder.title()}").classes(
                                "text-base font-semibold text-slate-200"
                            )
                            ui.label(f"{count} pages").classes("text-slate-400 text-sm mt-1")

            # All pages
            ui.label("All Pages").classes("text-lg font-semibold text-slate-200 mt-4")
            all_pages = store.get_all_pages()
            with ui.column().classes("w-full gap-2"):
                for page in all_pages:
                    with ui.link(target=page.url).classes("no-underline w-full"):
                        with ui.row().classes(
                            "w-full items-center gap-3 px-4 py-2 rounded-lg "
                            "hover:bg-slate-800 transition-colors"
                        ):
                            type_badge(page.type)
                            ui.label(page.title).classes("text-slate-200 text-sm")
                            ui.space()
                            ui.label(f"{len(page.outlinks)} links").classes(
                                "text-slate-500 text-xs"
                            )
