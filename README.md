# PKW Web

A Personal Knowledge Wiki browser built with [NiceGUI](https://nicegui.io/). Reads markdown files with YAML frontmatter from a local wiki directory and presents them in a searchable, linkable web interface with cross-references and backlinks.

## Disclaimer

This project is **vibecoded** — built through AI-assisted development (Claude) without manual review of every line of code. It is a personal tool for browsing a local knowledge wiki. **Do not use this in production environments.** There are no guarantees of security, stability, or correctness. Use at your own risk.

## Features

- **Wiki browser** — Browse 5 wiki categories: entities, concepts, sources, comparisons, syntheses
- **Wikilink resolution** — `[[slug]]` and `[[slug|Display Text]]` links resolve to clickable cross-references
- **Backlinks** — Each page shows which other pages link to it
- **Search** — Full-text search across titles, content, and tags (with 300ms debounce)
- **Sorting** — Sort page listings by name, in-links, out-links, or total links
- **Tag filtering** — Collapsible tag cloud filter; click tags on page items to filter directly
- **Dark/light mode** — Toggle in the header, preference persists across page navigation
- **Markdown rendering** — Headings, lists, tables, code blocks, blockquotes, and links

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- A wiki directory with markdown files (see [Wiki Format](#wiki-format))

## Quick Start

```bash
git clone https://github.com/Hopsakee/pkw-web.git
cd pkw-web
uv sync
uv run main.py
```

The app starts at http://localhost:8080 (or the port set via `APP_PORT`).

## Configuration

All settings are configurable via environment variables or a `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `WIKI_PATH` | `~/Drive/PKW/wiki` | Path to the wiki directory |
| `APP_TITLE` | `PKW — Personal Knowledge Wiki` | Browser tab title |
| `APP_HOST` | `0.0.0.0` | Bind address |
| `APP_PORT` | `8080` | Server port |
| `DARK_MODE` | `true` | Start in dark mode (`true`, `1`, `yes`, `on`) |

## Wiki Format

The app expects a wiki directory with this structure:

```
wiki/
├── entities/       # People, companies, tools, products
├── concepts/       # Ideas, frameworks, mental models
├── sources/        # Summaries of ingested sources
├── comparisons/    # Side-by-side analyses
└── syntheses/      # Cross-source theses
```

Each `.md` file should have YAML frontmatter:

```yaml
---
title: "Page Title"
type: entity
created: 2026-04-10
updated: 2026-04-10
tags: [ai, machine-learning, tools]
sources: ["source-slug"]
---

Content with [[wikilinks]] to other pages.
```

## Project Structure

```
pkw-web/
├── main.py                  # Entry point
├── pyproject.toml           # Dependencies (uv)
├── Dockerfile               # Container image (uv + Python 3.12)
├── compose.yaml             # Docker Compose for deployment
├── deploy.sh                # Hetzner VM deploy script
├── caddy-snippet.txt        # Caddy reverse proxy config
└── app/
    ├── config.py            # Settings from environment variables
    ├── wiki.py              # Wiki data loading, parsing, indexing
    ├── pages/
    │   ├── home.py          # Dashboard with folder cards and page list
    │   ├── folder.py        # Category page listing
    │   ├── page.py          # Individual wiki page view
    │   └── search.py        # Full-text search
    └── components/
        ├── layout.py        # Shared layout, header, CSS theming
        ├── badges.py        # Type badges (theme-aware)
        ├── markdown.py      # Markdown renderer with wikilink support
        └── page_list.py     # Sortable/filterable page list component
```

## Docker Deployment

The app is designed to run on a Hetzner VM with Caddy as reverse proxy and Authelia for authentication.

### Build and run locally with Docker

```bash
docker build -t pkw-web .
docker run -p 8080:8080 -v /path/to/wiki:/app/data/wiki:ro -e WIKI_PATH=/app/data/wiki pkw-web
```

### Deploy to Hetzner VM

1. Add the Caddy block from `caddy-snippet.txt` to your Caddyfile
2. Copy `compose.yaml` to `~/hopsakee-server/config/pkw-web/`
3. Ensure wiki data is mounted at `/mnt/HC_Volume_105122334/pkw-wiki/`
4. Run `deploy.sh` from the server setup directory

## Tech Stack

- **[NiceGUI](https://nicegui.io/)** — Python web UI framework (Quasar/Vue under the hood)
- **[httpx](https://www.python-httpx.org/)** — Async HTTP client
- **[python-frontmatter](https://github.com/eyeseast/python-frontmatter)** — YAML frontmatter parsing
- **[markdown](https://python-markdown.github.io/)** — Markdown to HTML conversion
- **[uv](https://docs.astral.sh/uv/)** — Python package manager

## License

MIT
