"""Render the website into a folder of static files."""

from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .assets import publish_assets
from .cards import Card, mana_symbol, read_cards, rules_to_html
from .devlog import load_posts
from .lore import GUILD_LORDS

WEBSITE = Path(__file__).resolve().parent.parent
TEMPLATES = WEBSITE / "templates"
STATIC = WEBSITE / "static"
DEVLOG = WEBSITE / "content" / "devlog"
DEFAULT_GAME_ASSETS = WEBSITE.parent / "shandalar-forever" / "assets" / "original"

# The cards in the native client's playable duel fixture.
FIRST_DUEL_CARDS = ("Ley Druid", "Healing Salve", "War Mammoth")

# Filters on the card gallery: (colour, mana symbol shown on the button).
COLOR_FILTERS = [
    ("white", "W"),
    ("blue", "U"),
    ("black", "B"),
    ("red", "R"),
    ("green", "G"),
    ("gold", None),
    ("artifact", None),
    ("land", None),
]


def build(out: Path, game_assets: Path = DEFAULT_GAME_ASSETS) -> None:
    cards = gallery_cards(game_assets)
    posts = load_posts(DEVLOG)

    out.mkdir(parents=True, exist_ok=True)
    publish_assets(game_assets / "converted", out, cards)
    shutil.copytree(STATIC, out, dirs_exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["rules"] = rules_to_html
    env.filters["mana"] = mana_symbol
    env.globals["lords"] = GUILD_LORDS

    cards_by_name = {card.name: card for card in cards}
    pages = {
        "index.html": (
            "index.html",
            {
                "first_duel": [cards_by_name[name] for name in FIRST_DUEL_CARDS],
                "card_count": len(cards),
                "latest_posts": posts[:2],
            },
        ),
        "world.html": ("world.html", {}),
        "cards.html": ("cards.html", {"cards": cards, "color_filters": COLOR_FILTERS}),
        "devlog.html": ("devlog.html", {"posts": posts}),
    }
    for post in posts:
        pages[f"devlog/{post.slug}.html"] = ("post.html", {"post": post})

    for path, (template, context) in pages.items():
        html = env.get_template(template).render(
            page=path,
            root="../" * path.count("/"),
            **context,
        )
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    print(f"Built {len(pages)} pages and {len(cards)} cards into {out}")


def gallery_cards(game_assets: Path) -> list[Card]:
    """Cards that have their own illustration, sorted by name."""
    art_folder = game_assets / "converted" / "CardArt" / "medart"
    cards = [
        card
        for card in read_cards(game_assets / "raw" / "CARDS.DAT")
        if (art_folder / f"{card.art}.png").exists() and has_own_art(card)
    ]
    return sorted(cards, key=lambda card: card.name)


def has_own_art(card: Card) -> bool:
    # Cards without an illustration point at the first art file as a placeholder.
    return card.art != "0000" or card.id == 0
