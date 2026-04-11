"""Type badge component for wiki page types."""

from nicegui import ui

from app.wiki import TYPE_CONFIG

# Type colors that work in both dark and light mode
_TYPE_COLORS: dict[str, dict[str, str]] = {
    "entity": {
        "dark_bg": "#1e3a5f", "dark_text": "#93c5fd",
        "light_bg": "#dbeafe", "light_text": "#1e40af",
    },
    "concept": {
        "dark_bg": "#3b1f6e", "dark_text": "#c4b5fd",
        "light_bg": "#ede9fe", "light_text": "#5b21b6",
    },
    "source": {
        "dark_bg": "#14412a", "dark_text": "#86efac",
        "light_bg": "#dcfce7", "light_text": "#166534",
    },
    "comparison": {
        "dark_bg": "#4a2410", "dark_text": "#fdba74",
        "light_bg": "#ffedd5", "light_text": "#9a3412",
    },
    "synthesis": {
        "dark_bg": "#4a1942", "dark_text": "#f9a8d4",
        "light_bg": "#fce7f3", "light_text": "#9d174d",
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
