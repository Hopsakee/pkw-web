"""Custom markdown renderer with wikilink support."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import markdown as md

if TYPE_CHECKING:
    from app.wiki import WikiStore

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def render_wiki_markdown(content: str, store: WikiStore) -> str:
    """Convert wiki markdown to HTML, resolving [[wikilinks]] to real links."""

    def replace_wikilink(match: re.Match) -> str:
        slug = match.group(1).strip()
        display = match.group(2) or slug.replace("-", " ").title()
        resolved = store.resolve_slug(slug)
        if resolved:
            folder, s = resolved
            return f'<a href="/wiki/{folder}/{s}" class="wikilink">{display}</a>'
        return f'<span class="wikilink-broken">{display}</span>'

    processed = WIKILINK_RE.sub(replace_wikilink, content)

    html = md.markdown(
        processed,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    return html
