"""Load dev log posts from Markdown files.

Each post starts with a few "key: value" lines, then a line with three dashes,
then the Markdown body:

    title: The first duel
    date: 2026-10-20
    summary: One sentence shown in the post list.
    ---
    Post body...
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import markdown
from markupsafe import Markup


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    date: date
    summary: str
    body: Markup


def load_posts(folder: Path) -> list[Post]:
    """Return all posts, newest first."""
    posts = [read_post(path) for path in folder.glob("*.md")]
    return sorted(posts, key=lambda post: post.date, reverse=True)


def read_post(path: Path) -> Post:
    header, body = path.read_text(encoding="utf-8").split("\n---\n", maxsplit=1)
    fields = dict(line.split(": ", maxsplit=1) for line in header.splitlines() if line)
    return Post(
        slug=path.stem,
        title=fields["title"],
        date=date.fromisoformat(fields["date"]),
        summary=fields["summary"],
        body=Markup(markdown.markdown(body, extensions=["fenced_code", "tables"])),
    )
