"""Wiki data loading: scan folders, parse frontmatter, compute links."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

WIKI_FOLDERS = ("entities", "concepts", "sources", "comparisons", "syntheses")

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

TYPE_CONFIG: dict[str, dict[str, str]] = {
    "entity":     {"icon": "\U0001F464", "color": "#3b82f6"},  # blue
    "concept":    {"icon": "\U0001F4A1", "color": "#a855f7"},  # purple
    "source":     {"icon": "\U0001F4C4", "color": "#22c55e"},  # green
    "comparison": {"icon": "\u2696\ufe0f", "color": "#f97316"},  # orange
    "synthesis":  {"icon": "\U0001F9EC", "color": "#ec4899"},  # pink
}

FOLDER_TO_TYPE = {
    "entities": "entity",
    "concepts": "concept",
    "sources": "source",
    "comparisons": "comparison",
    "syntheses": "synthesis",
}


@dataclass(slots=True)
class WikiPage:
    slug: str
    folder: str
    title: str
    type: str
    created: str
    updated: str
    tags: list[str]
    sources: list[str]
    content: str
    outlinks: list[str] = field(default_factory=list)
    backlinks: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"/wiki/{self.folder}/{self.slug}"

    @property
    def snippet(self) -> str:
        text = self.content.strip()
        text = re.sub(r"^#+\s+.*$", "", text, flags=re.MULTILINE).strip()
        text = WIKILINK_RE.sub(r"\1", text)
        return text[:200] + "..." if len(text) > 200 else text


@dataclass(slots=True)
class WikiStats:
    total_pages: int = 0
    entities: int = 0
    concepts: int = 0
    sources: int = 0
    comparisons: int = 0
    syntheses: int = 0
    total_links: int = 0


class WikiStore:
    """Loads and indexes all wiki pages from disk."""

    def __init__(self, wiki_path: Path) -> None:
        self.wiki_path = wiki_path
        self.pages: dict[str, WikiPage] = {}
        self._slug_to_folder: dict[str, str] = {}

    def load(self) -> None:
        self.pages.clear()
        self._slug_to_folder.clear()

        for folder_name in WIKI_FOLDERS:
            folder = self.wiki_path / folder_name
            if not folder.is_dir():
                continue
            for md_file in sorted(folder.glob("*.md")):
                page = self._parse_file(md_file, folder_name)
                if page:
                    key = f"{folder_name}/{page.slug}"
                    self.pages[key] = page
                    self._slug_to_folder[page.slug] = folder_name

        self._compute_backlinks()

    def _parse_file(self, path: Path, folder_name: str) -> WikiPage | None:
        try:
            post = frontmatter.load(str(path))
        except Exception:
            return None

        slug = path.stem
        meta = post.metadata
        wiki_type = FOLDER_TO_TYPE.get(folder_name, folder_name)
        content = post.content

        outlinks = WIKILINK_RE.findall(content)

        return WikiPage(
            slug=slug,
            folder=folder_name,
            title=meta.get("title", slug.replace("-", " ").title()),
            type=meta.get("type", wiki_type),
            created=str(meta.get("created", "")),
            updated=str(meta.get("updated", "")),
            tags=meta.get("tags", []) or [],
            sources=meta.get("sources", []) or [],
            content=content,
            outlinks=outlinks,
        )

    def _compute_backlinks(self) -> None:
        for page in self.pages.values():
            for link_slug in page.outlinks:
                folder = self._slug_to_folder.get(link_slug)
                if folder:
                    target_key = f"{folder}/{link_slug}"
                    target = self.pages.get(target_key)
                    if target and page.slug not in target.backlinks:
                        target.backlinks.append(page.slug)

    def get_page(self, folder: str, slug: str) -> WikiPage | None:
        return self.pages.get(f"{folder}/{slug}")

    def get_folder_pages(self, folder: str) -> list[WikiPage]:
        return sorted(
            [p for p in self.pages.values() if p.folder == folder],
            key=lambda p: p.title.lower(),
        )

    def get_all_pages(self) -> list[WikiPage]:
        return sorted(self.pages.values(), key=lambda p: p.title.lower())

    def get_stats(self) -> WikiStats:
        stats = WikiStats(total_pages=len(self.pages))
        for page in self.pages.values():
            if page.folder == "entities": stats.entities += 1
            elif page.folder == "concepts": stats.concepts += 1
            elif page.folder == "sources": stats.sources += 1
            elif page.folder == "comparisons": stats.comparisons += 1
            elif page.folder == "syntheses": stats.syntheses += 1
            stats.total_links += len(page.outlinks)
        return stats

    def search(self, query: str) -> list[WikiPage]:
        q = query.lower()
        results = []
        for page in self.pages.values():
            if (q in page.title.lower()
                or q in page.content.lower()
                or any(q in tag.lower() for tag in page.tags)):
                results.append(page)
        return sorted(results, key=lambda p: p.title.lower())

    def resolve_slug(self, slug: str) -> tuple[str, str] | None:
        folder = self._slug_to_folder.get(slug)
        if folder:
            return folder, slug
        return None
