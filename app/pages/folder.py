"""Folder view: list all pages in a wiki category."""

from nicegui import ui

from app.components.badges import type_badge
from app.components.layout import page_layout
from app.config import Settings
from app.wiki import FOLDER_TO_TYPE, TYPE_CONFIG, WIKI_FOLDERS, WikiStore


def register(store: WikiStore, settings: Settings) -> None:

    @ui.page("/wiki/{folder}")
    def folder_page(folder: str) -> None:
        if folder not in WIKI_FOLDERS:
            with page_layout("Not Found"):
                ui.label(f"Unknown folder: {folder}").classes("text-red-400")
            return

        pages = store.get_folder_pages(folder)
        wiki_type = FOLDER_TO_TYPE[folder]
        cfg = TYPE_CONFIG.get(wiki_type, {})

        with page_layout(folder.title()):
            # Header
            with ui.row().classes("items-center gap-3"):
                ui.label(f"{cfg.get('icon', '')} {folder.title()}").classes(
                    "text-2xl font-bold text-slate-100"
                )
                ui.badge(f"{len(pages)} pages").classes("text-white").props(
                    f'color="{cfg.get("color", "#6b7280")}"'
                )

            # Page list
            with ui.column().classes("w-full gap-2"):
                for page in pages:
                    with ui.link(target=page.url).classes("no-underline w-full"):
                        with ui.element("div").classes(
                            "wiki-card flex items-center gap-4"
                        ):
                            with ui.column().classes("flex-1 gap-1"):
                                ui.label(page.title).classes(
                                    "text-slate-200 font-medium text-sm"
                                )
                                if page.snippet:
                                    ui.label(page.snippet[:120]).classes(
                                        "text-slate-500 text-xs"
                                    )
                            with ui.row().classes("gap-3 items-center"):
                                if page.tags:
                                    for tag in page.tags[:3]:
                                        ui.badge(tag).classes(
                                            "text-xs bg-slate-700 text-slate-300"
                                        )
                                with ui.column().classes("items-end gap-0"):
                                    ui.label(f"{len(page.outlinks)} out").classes(
                                        "text-slate-500 text-xs"
                                    )
                                    ui.label(f"{len(page.backlinks)} back").classes(
                                        "text-slate-500 text-xs"
                                    )
