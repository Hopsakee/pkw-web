"""Shared layout: header, navigation, page wrapper."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from nicegui import ui

APP_CSS = """
:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --accent: #38bdf8;
    --accent-hover: #7dd3fc;
    --border: #334155;
}

body {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', 'system-ui', sans-serif;
}

.q-page { background-color: var(--bg-primary) !important; }
.q-layout { background-color: var(--bg-primary) !important; }

.wiki-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    transition: border-color 0.2s, transform 0.15s;
}
.wiki-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}

.stat-card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: center;
}

.wiki-content h1 { font-size: 1.75rem; font-weight: 700; margin: 1.5rem 0 0.75rem; color: var(--text-primary); }
.wiki-content h2 { font-size: 1.35rem; font-weight: 600; margin: 1.25rem 0 0.5rem; color: var(--text-primary); }
.wiki-content h3 { font-size: 1.1rem; font-weight: 600; margin: 1rem 0 0.5rem; color: var(--text-primary); }
.wiki-content p { margin: 0.5rem 0; line-height: 1.7; color: var(--text-secondary); }
.wiki-content ul, .wiki-content ol { margin: 0.5rem 0; padding-left: 1.5rem; color: var(--text-secondary); }
.wiki-content li { margin: 0.25rem 0; line-height: 1.6; }
.wiki-content blockquote {
    border-left: 3px solid var(--accent);
    padding: 0.5rem 1rem;
    margin: 0.75rem 0;
    color: var(--text-secondary);
    background-color: rgba(56, 189, 248, 0.05);
    border-radius: 0 8px 8px 0;
}
.wiki-content code {
    background-color: var(--bg-primary);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-size: 0.875em;
    color: var(--accent);
}
.wiki-content pre {
    background-color: var(--bg-primary);
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
.wiki-content th { background-color: var(--bg-primary); font-weight: 600; }
.wiki-content hr { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

.wiki-content a.wikilink {
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px dotted var(--accent);
    transition: color 0.2s;
}
.wiki-content a.wikilink:hover { color: var(--accent-hover); }
.wiki-content .wikilink-broken {
    color: #6b7280;
    text-decoration: line-through;
    cursor: not-allowed;
}
.wiki-content a {
    color: var(--accent);
    text-decoration: none;
}
.wiki-content a:hover { color: var(--accent-hover); text-decoration: underline; }

.sidebar-link {
    color: var(--accent);
    cursor: pointer;
    font-size: 0.875rem;
    transition: color 0.2s;
}
.sidebar-link:hover { color: var(--accent-hover); }

.search-input .q-field__control {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
"""


def add_head_html() -> None:
    ui.add_head_html(f"<style>{APP_CSS}</style>")
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )


def header() -> None:
    with ui.header().classes("bg-slate-900 border-b border-slate-700"):
        with ui.row().classes("w-full items-center px-6 py-2"):
            ui.link("PKW", "/").classes(
                "text-xl font-bold text-sky-400 no-underline hover:text-sky-300"
            )
            ui.space()
            for label, href in [
                ("Home", "/"),
                ("Search", "/search"),
            ]:
                ui.link(label, href).classes(
                    "text-slate-300 no-underline hover:text-sky-400 text-sm"
                )
            for folder in ("entities", "concepts", "sources", "comparisons", "syntheses"):
                ui.link(
                    folder.title(), f"/wiki/{folder}"
                ).classes("text-slate-400 no-underline hover:text-sky-400 text-sm")


@contextmanager
def page_layout(title: str = "") -> Generator[None, None, None]:
    add_head_html()
    if title:
        ui.page_title(f"{title} — PKW")
    header()
    with ui.column().classes("w-full max-w-6xl mx-auto px-6 py-8 gap-6"):
        yield
