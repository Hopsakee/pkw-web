"""Type badge component for wiki page types."""

from nicegui import ui

from app.wiki import TYPE_CONFIG


def type_badge(wiki_type: str) -> None:
    cfg = TYPE_CONFIG.get(wiki_type, {"icon": "?", "color": "#6b7280"})
    ui.badge(
        f"{cfg['icon']} {wiki_type}",
        color=cfg["color"],
    ).classes("text-white text-xs px-2 py-1")
