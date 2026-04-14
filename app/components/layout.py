"""Shared layout: header, navigation, page wrapper."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from nicegui import app, ui

APP_CSS = """
:root, body.body--light {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --bg-card: #075895;
    --card-text: #ffffff;
    --card-text-muted: rgba(255, 255, 255, 0.7);
    --text-primary: #333333;
    --text-secondary: #6f6f6f;
    --text-muted: #999999;
    --accent: #075895;
    --accent-hover: #f29100;
    --accent-orange-light: #fff4e0;
    --border: #075895;
    --hover-bg: rgba(7, 88, 149, 0.06);
    --header-bg: #ffffff;
    --badge-bg: rgba(7, 88, 149, 0.08);
    --badge-text: #075895;
    --badge-border: rgba(7, 88, 149, 0.15);
    --tag-bg: #e8f0f7;
    --tag-text: #075895;
    --tag-border: #075895;
    --tag-active-bg: #f29100;
    --tag-active-text: #ffffff;
}

body.body--dark {
    --bg-primary: #0a2540;
    --bg-secondary: #0e3358;
    --bg-card: #0e3358;
    --card-text: #e8edf2;
    --card-text-muted: #6b8aaa;
    --text-primary: #e8edf2;
    --text-secondary: #a0b4c8;
    --text-muted: #6b8aaa;
    --accent: #00b0ea;
    --accent-hover: #f29100;
    --accent-orange-light: #1a1400;
    --border: #1a4570;
    --hover-bg: rgba(0, 176, 234, 0.08);
    --header-bg: #0a2540;
    --badge-bg: rgba(0, 176, 234, 0.12);
    --badge-text: #a0d8ef;
    --badge-border: rgba(0, 176, 234, 0.2);
    --tag-bg: #0e3358;
    --tag-text: #a0b4c8;
    --tag-border: #1a4570;
    --tag-active-bg: #075895;
    --tag-active-text: #ffffff;
}

body {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: Arial, Helvetica, sans-serif;
}

.q-page { background-color: var(--bg-primary) !important; }
.q-layout { background-color: var(--bg-primary) !important; }

.wiki-card {
    background-color: var(--bg-card);
    color: var(--card-text);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    transition: border-color 0.2s, transform 0.15s;
}
.wiki-card:hover {
    border-color: var(--accent-hover);
    transform: translateY(-2px);
}

.filter-panel {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* Wiki content typography — headings use WDODelta accent blue */
.wiki-content h1 { font-size: 1.75rem; font-weight: 700; margin: 1.5rem 0 0.75rem; color: var(--accent); }
.wiki-content h2 { font-size: 1.35rem; font-weight: 600; margin: 1.25rem 0 0.5rem; color: var(--accent); }
.wiki-content h3 { font-size: 1.1rem; font-weight: 600; margin: 1rem 0 0.5rem; color: var(--accent); }
.wiki-content p { margin: 0.5rem 0; line-height: 1.7; color: var(--text-secondary); }

/* Lists — explicit bullet/number styles */
.wiki-content ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
    color: var(--text-secondary);
    list-style-type: disc;
}
.wiki-content ol {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
    color: var(--text-secondary);
    list-style-type: decimal;
}
.wiki-content ul ul { list-style-type: circle; }
.wiki-content ul ul ul { list-style-type: square; }
.wiki-content li {
    margin: 0.25rem 0;
    line-height: 1.6;
    display: list-item;
}

.wiki-content blockquote {
    border-left: 3px solid var(--accent);
    padding: 0.5rem 1rem;
    margin: 0.75rem 0;
    color: var(--text-secondary);
    background-color: var(--accent-orange-light);
    border-radius: 0 8px 8px 0;
}
.wiki-content code {
    background-color: var(--bg-secondary);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-size: 0.875em;
    color: var(--accent);
}
.wiki-content pre {
    background-color: var(--bg-secondary);
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid var(--border);
}
.wiki-content pre code { background: none; padding: 0; color: var(--text-secondary); }
.wiki-content table { border-collapse: collapse; width: 100%; margin: 0.75rem 0; }
.wiki-content th, .wiki-content td {
    border: 1px solid var(--border);
    padding: 0.5rem 0.75rem;
    text-align: left;
}
.wiki-content th { background-color: var(--bg-secondary); font-weight: 600; }
.wiki-content hr { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

.wiki-content a.wikilink {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px dotted var(--accent);
    transition: color 0.2s;
}
.wiki-content a.wikilink:hover { color: var(--accent-hover); }
.wiki-content .wikilink-broken {
    color: var(--text-muted);
    text-decoration: line-through;
    cursor: not-allowed;
}
.wiki-content a { color: var(--accent); text-decoration: none; }
.wiki-content a:hover { color: var(--accent-hover); text-decoration: underline; }

.sidebar-link {
    color: var(--card-text) !important;
    cursor: pointer;
    font-size: 0.875rem;
    transition: opacity 0.2s;
}
.sidebar-link:hover { opacity: 0.8; }

.search-input .q-field__control {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* Tag cloud */
.tag-pill {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s;
    background-color: var(--tag-bg);
    color: var(--tag-text);
    border: 1px solid var(--tag-border);
}
.tag-pill:hover {
    border-color: var(--accent);
    color: var(--accent);
}
.tag-pill-active {
    background-color: var(--tag-active-bg) !important;
    color: var(--tag-active-text) !important;
    border-color: var(--tag-active-bg) !important;
}

/* Sort select styling */
.sort-select .q-field__control {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    min-height: 36px !important;
}
.sort-select .q-field__label {
    color: var(--text-muted) !important;
}
.sort-select .q-field__native,
.sort-select .q-field__input {
    color: var(--text-primary) !important;
}

/* Header theming */
.pkw-header {
    background-color: var(--header-bg) !important;
    border-bottom: none !important;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.10) !important;
}
.pkw-header-logo {
    height: 40px;
    width: 160px;
}
.pkw-header-logo .q-img__image {
    object-fit: contain !important;
    object-position: left center !important;
}
"""


LOGO_URL = "/static/data/wdod_logo_uw_cmyk_pc_friendly_1.svg"


def add_head_html() -> None:
    ui.add_head_html(f"<style>{APP_CSS}</style>")


def header() -> None:
    with ui.header().classes("pkw-header"):
        with ui.row().classes("w-full items-center px-6 py-2"):
            with ui.link(target="/").classes("no-underline"):
                ui.image(LOGO_URL).classes("pkw-header-logo")
            ui.space()
            for label, href in [
                ("Home", "/"),
                ("Search", "/search"),
            ]:
                ui.link(label, href).classes(
                    "no-underline text-sm font-medium"
                ).style("color: var(--accent)")
            for folder in ("entities", "concepts", "sources", "comparisons", "syntheses"):
                ui.link(
                    folder.title(), f"/wiki/{folder}"
                ).classes("no-underline text-sm").style("color: var(--text-secondary)")

            # Dark mode toggle — persisted via app.storage.user
            is_dark = app.storage.user.get("dark_mode", True)
            dark = ui.dark_mode(value=is_dark)

            def toggle_dark() -> None:
                dark.toggle()
                app.storage.user["dark_mode"] = dark.value

            icon = "light_mode" if is_dark else "dark_mode"
            ui.button(
                icon=icon,
                on_click=toggle_dark,
            ).props("flat round size=sm").style("color: var(--text-secondary)")


@contextmanager
def page_layout(title: str = "") -> Generator[None, None, None]:
    add_head_html()
    if title:
        ui.page_title(f"{title} — PKW")
    header()
    with ui.column().classes("w-full max-w-6xl mx-auto px-6 py-8 gap-6"):
        yield
