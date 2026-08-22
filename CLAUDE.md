# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync              # Install dependencies
uv run main.py       # Start dev server at http://localhost:8081
uv run pytest        # Run tests (no tests exist yet)

# With custom wiki path
WIKI_PATH=/path/to/wiki uv run main.py

# Docker
docker build -t pkw-web .
docker run -p 8080:8080 -v /path/to/wiki:/app/data/wiki:ro -e WIKI_PATH=/app/data/wiki pkw-web
```

## Architecture

NiceGUI web app (Python 3.12, Quasar/Vue underneath) that reads a local directory of markdown files with YAML frontmatter and serves them as a wiki with cross-references.

### Data flow

1. `WikiStore.load()` scans 5 wiki folders (`entities/`, `concepts/`, `sources/`, `comparisons/`, `syntheses/`), parses frontmatter + wikilinks, computes backlinks, and precomputes all indexes **once at startup**
2. Page handlers read from the in-memory store — no disk I/O per request
3. `render_wiki_markdown()` resolves `[[slug]]` and `[[slug|display]]` wikilinks to HTML links at render time

### Page registration pattern

Each page module exports `register(store, settings)` which decorates handlers with `@ui.page("/path")`. All four are registered in `main.py`.

### Theming

All colors use CSS variables defined in `layout.py`'s `APP_CSS`. Two scopes: `:root, body.body--light` (light) and `body.body--dark` (dark). NiceGUI's `ui.dark_mode()` toggles the body class. Dark mode preference persists via `app.storage.user["dark_mode"]`.

WDODelta brand palette: `#075895` (blue), `#00b0ea` (light blue), `#f29100` (orange), `#93c01f` (green), `#d74116` (red).

### Key variables for card content

Cards (`wiki-card`) use `--bg-card` as background (blue in light mode). Use `--card-text` and `--card-text-muted` for text inside cards — not `--text-primary`, which is for page-level content.

## Conventions

- **uv only** — never add dependencies via pip
- **CSS variables for all colors** — never hardcode colors; use `var(--text-primary)`, `var(--bg-card)`, etc.
- **Test both dark and light mode** after any visual change
- **Type hints** throughout
- **Pathlib** for file operations
- Pages go in `app/pages/`, reusable UI in `app/components/`, data logic in `app/wiki.py`

## Deployment

Runs on a Hetzner VM behind Caddy (reverse proxy) + Authelia (auth). Wiki data is mounted read-only from a Hetzner volume. Config files live at `~/hopsakee-server/config/pkw-web/`. Deploy via `deploy.sh`.

## Vibecoded

This project was AI-assisted without manual review of every line. It is a personal tool, not production software.
