"""Home page: folder cards + sortable/filterable page list."""

from nicegui import ui

from app.components.layout import page_layout
from app.components.page_list import page_list_controls
from app.config import Settings
from app.wiki import FOLDER_TO_TYPE, TYPE_CONFIG, WIKI_FOLDERS, WikiStore


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/")
    def home_page() -> None:
        with page_layout("Home"):
            stats = store.get_stats()

            ui.label("Personal Knowledge Wiki").style(
                "color: var(--text-primary); font-size: 1.875rem; font-weight: 700"
            )
            ui.label(
                f"{stats.total_pages} pages \u00b7 {stats.total_links} cross-references"
            ).style("color: var(--text-muted); font-size: 0.875rem; margin-top: -1rem")

            # Folder cards
            with ui.row().classes("w-full gap-4 flex-wrap"):
                for folder in WIKI_FOLDERS:
                    wiki_type = FOLDER_TO_TYPE[folder]
                    cfg = TYPE_CONFIG.get(wiki_type, {})
                    count = stats.counts.get(folder, 0)
                    with ui.link(target=f"/wiki/{folder}").classes("no-underline flex-1 min-w-[180px]"):
                        with ui.element("div").classes("wiki-card cursor-pointer"):
                            ui.label(f"{cfg.get('icon', '')} {folder.title()}").style(
                                "color: var(--card-text); font-size: 1rem; font-weight: 600"
                            )
                            ui.label(f"{count} pages").style(
                                "color: var(--card-text-muted); font-size: 0.875rem; margin-top: 0.25rem"
                            )

            # All pages with sort + filter
            ui.label("All Pages").style(
                "color: var(--text-primary); font-size: 1.125rem; font-weight: 600; margin-top: 1rem"
            )
            page_list_controls(store.get_all_pages(), store)
