"""Render the website into a folder of static files."""

from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .assets import publish_assets
from .bestiary import group_by_homeland, load_creatures
from .cards import Card, mana_symbol, read_cards, rules_to_html
from .devlog import load_posts
from .lore import GUILD_LORDS, PLACES, TERRAINS, WORLD_MAGICS

WEBSITE = Path(__file__).resolve().parent.parent
TEMPLATES = WEBSITE / "templates"
STATIC = WEBSITE / "static"
DEVLOG = WEBSITE / "content" / "devlog"
CREATURES = WEBSITE / "content" / "creatures.csv"
SCREENSHOTS = WEBSITE / "content" / "screenshots"

# Screenshots of the current browser build, shown on the home page:
# (file in content/screenshots/, caption). The first one is shown largest.
SCREENSHOT_CAPTIONS = [
    ("overworld.webp", "Exploring the overworld"),
    ("duel.webp", "A duel"),
    ("title-menu.webp", "The title screen"),
    ("choose-your-visage.webp", "Choosing your visage"),
]
# The game files the site uses, copied from the game repository by
# scripts/sync_game_assets.py.
DEFAULT_GAME_ASSETS = WEBSITE / "game-assets"

# Links shown on the download page. While a link is empty, the page says it is
# coming soon instead of showing a broken button.
DOWNLOADS = {
    "Linux": "",
    "Windows": "",
}
GITHUB_URL = ""

# Minimum requirements, taken from the Fyrox engine the game is built on:
# Fyrox 1.0 needs OpenGL 3.3 (or OpenGL ES 3.0), and Rust's 64-bit Windows
# target needs Windows 10 or later.
REQUIREMENTS = [
    ("Operating system", "Windows 10 or later (64-bit), or Linux with X11 or Wayland"),
    ("Graphics", "A graphics card and driver supporting OpenGL 3.3 or OpenGL ES 3.0"),
    ("Processor", "64-bit (x86-64)"),
]

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
    creatures = load_creatures(
        CREATURES, game_assets / "raw" / "DECKS", read_cards(game_assets / "raw" / "CARDS.DAT")
    )
    posts = load_posts(DEVLOG)

    out.mkdir(parents=True, exist_ok=True)
    publish_assets(game_assets / "converted", out, cards, creatures)
    shutil.copytree(STATIC, out, dirs_exist_ok=True)
    shutil.copytree(SCREENSHOTS, out / "img" / "screenshots", dirs_exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["rules"] = rules_to_html
    env.filters["mana"] = mana_symbol
    env.globals["lords"] = GUILD_LORDS

    pages = {
        "index.html": (
            "index.html",
            {"latest_posts": posts[:2], "screenshots": SCREENSHOT_CAPTIONS},
        ),
        "world.html": (
            "world.html",
            {
                "terrains": TERRAINS,
                "places": PLACES,
                "world_magics": WORLD_MAGICS,
                "land_art": {card.name: card.art for card in cards},
            },
        ),
        "download.html": (
            "download.html",
            {"downloads": DOWNLOADS, "github_url": GITHUB_URL, "requirements": REQUIREMENTS},
        ),
        "bestiary.html": (
            "bestiary.html",
            {
                "homelands": group_by_homeland(creatures),
                "previewable_cards": {card.id for card in cards},
            },
        ),
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
