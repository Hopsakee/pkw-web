"""Type badge component for wiki page types."""

from nicegui import ui

from app.wiki import TYPE_CONFIG

# Ensure badge text is readable against each type's background color
_BADGE_TEXT_COLORS: dict[str, str] = {
    "entity": "#ffffff",
    "concept": "#ffffff",
    "source": "#ffffff",
    "comparison": "#ffffff",
    "synthesis": "#ffffff",
}

# Darker background variants for better contrast
_BADGE_BG_COLORS: dict[str, str] = {
    "entity": "#2563eb",      # darker blue (was #3b82f6)
    "concept": "#7c3aed",     # darker purple (was #a855f7)
    "source": "#16a34a",      # darker green (was #22c55e)
    "comparison": "#ea580c",  # darker orange (was #f97316)
    "synthesis": "#db2777",   # darker pink (was #ec4899)
}


def type_badge(wiki_type: str) -> None:
    bg = _BADGE_BG_COLORS.get(wiki_type, "#4b5563")
    text = _BADGE_TEXT_COLORS.get(wiki_type, "#ffffff")
    cfg = TYPE_CONFIG.get(wiki_type, {"icon": "?"})
    ui.badge(
        f"{cfg['icon']} {wiki_type}",
    ).style(
        f"background-color: {bg}; color: {text}; font-weight: 500"
    ).classes("text-xs px-2 py-1")
