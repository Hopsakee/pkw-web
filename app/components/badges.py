"""Type badge component for wiki page types."""

from nicegui import ui

from app.wiki import TYPE_CONFIG

# Type colors derived from WDODelta palette:
# #075895 (blue), #00b0ea (light blue), #f29100 (orange), #93c01f (green), #d74116 (red)
_TYPE_COLORS: dict[str, dict[str, str]] = {
    "entity": {
        "dark_bg": "#0a3a60", "dark_text": "#7dc8f5",
        "light_bg": "#e3f0fa", "light_text": "#075895",
    },
    "concept": {
        "dark_bg": "#0b4a6e", "dark_text": "#6dd4f5",
        "light_bg": "#ddf3fc", "light_text": "#007bb8",
    },
    "source": {
        "dark_bg": "#2a4a0a", "dark_text": "#c2e06a",
        "light_bg": "#eef6d8", "light_text": "#5a7a0d",
    },
    "comparison": {
        "dark_bg": "#5a3500", "dark_text": "#f5be5a",
        "light_bg": "#fef0d5", "light_text": "#b07000",
    },
    "synthesis": {
        "dark_bg": "#5a1a0a", "dark_text": "#f58a6a",
        "light_bg": "#fde8e2", "light_text": "#d74116",
    },
}


def type_badge(wiki_type: str) -> None:
    cfg = TYPE_CONFIG.get(wiki_type, {"icon": "?"})
    colors = _TYPE_COLORS.get(wiki_type, {
        "dark_bg": "#374151", "dark_text": "#d1d5db",
        "light_bg": "#f3f4f6", "light_text": "#374151",
    })
    ui.html(
        f'<span class="type-badge type-badge-{wiki_type}">'
        f'{cfg["icon"]} {wiki_type}</span>'
    )
    # Inject per-type CSS using body class selectors
    ui.add_head_html(f"""<style>
    body.body--dark .type-badge-{wiki_type} {{
        background-color: {colors["dark_bg"]};
        color: {colors["dark_text"]};
    }}
    body.body--light .type-badge-{wiki_type} {{
        background-color: {colors["light_bg"]};
        color: {colors["light_text"]};
    }}
    .type-badge {{
        display: inline-block;
        padding: 0.15rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        white-space: nowrap;
    }}
    </style>""")
