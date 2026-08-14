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

Runs on a Hetzner VM behind Caddy (reverse proxy). Public at
`datalab-knowledge.hopsakee.top`, routed with **no Authelia gate** —
deliberately public/read-only (F13 decision, 2026-07-03). Wiki data is
mounted read-only from a Hetzner volume. Config files live at
`~/hopsakee-server/config/pkw-web/`. Deploy via `deploy.sh`.

## Refresh Contract — rsync new wiki content, then restart

`WikiStore.load()` runs ONCE at process startup. New files arriving in the
bind-mount source are visible from inside the container but the in-memory
`store.pages` dict is frozen at boot. After every meaningful rsync the
container has to be restarted:

```bash
# Both sides reference wiki/ explicitly — symmetric trailing slashes:
rsync -avh --delete -e 'ssh -i ~/.ssh/sledge_wsl' \
  ~/Drive/wiki_beleid/wiki/ \
  ubuntu@hopsakee.top:/mnt/HC_Volume_105122334/pkw-wiki/wiki/

ssh -i ~/.ssh/sledge_wsl ubuntu@hopsakee.top 'docker restart pkw-web'
```

A `/_reload` endpoint avoids the container restart:

```bash
curl -fsS -X POST -H "X-Reload-Token: $RELOAD_TOKEN" \
  https://datalab-knowledge.hopsakee.top/_reload
```

The handler rebuilds the wiki store into a fresh `WikiStore`, then atomically
swaps the in-memory state on the live store. On `load()` failure the previous
state is left untouched and the endpoint returns 500. Success returns JSON
with `status`, `pages`, `delta`, `elapsed_ms`, and `loaded_at`.

**Operator note:** `RELOAD_TOKEN` (or `RELOAD_TOKEN_FILE`, Authelia-style)
MUST be set in the deployed env (the `pkw-web` compose `environment:` block
on the Hetzner VM — not yet added there as of this port). When unset the
endpoint returns 503 on every call. Tokens shorter than 16 chars trigger a
startup warning. The token is read at startup and stripped of surrounding
whitespace; `X-Reload-Token` header is compared via `hmac.compare_digest`.
A repeat call within `RELOAD_MIN_INTERVAL_S` (default 30s) gets 429.

**Security note — this domain has NO Authelia gate.** Unlike hopswiki-web,
`datalab-knowledge.hopsakee.top` is routed in Caddy with no
`authelia_forward_auth` import. That means the `RELOAD_TOKEN` check in the
handler is the *only* access control on this endpoint, not a second layer
behind a cookie gate. Use a long, random token and treat it with the same
care as any internet-facing secret.

## Vibecoded

This project was AI-assisted without manual review of every line. It is a personal tool, not production software.
