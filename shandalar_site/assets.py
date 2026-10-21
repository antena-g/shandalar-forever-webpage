"""Prepare the original game art that the website uses.

Everything is read from the game's converted assets folder and written into the
build folder. Nothing in the game folder is modified.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

from .bestiary import Creature
from .cards import Card
from .lore import GUILD_LORDS, PLACES, TERRAINS

# Published path -> source path inside assets/original/converted/.
GAME_ART = {
    "img/title.webp": "TITLE.png",
    "img/celeb.webp": "CELEB.png",
    "img/cave.webp": "CAVEBKGD.png",
    "img/cavern.webp": "CLUEBACK.png",
    "img/spellbook.webp": "staceybk.png",
    "img/castle-dusk.webp": "NEWSBACK.png",
    "img/castle.webp": "0028.png",
    "img/spirit-forest.webp": "0335.png",
    "img/standing-stones.webp": "0364.png",
    "img/emblem.png": "DBArt/ASTRAL.png",  # The Astral set icon: cards native to Shandalar.
    "img/mana-symbols.png": "CardArt/ManaSymbolsMasked.png",
    "img/card-back.webp": "CardArt/CARDBACK.png",
    "img/button.png": "DuelArt/WINBK_StartDuelButtonNormal.png",
    "img/button-pressed.png": "DuelArt/WINBK_StartDuelButtonDepressed.png",
    "img/button-disabled.png": "DuelArt/WINBK_StartDuelButtonDisabled.png",
    "img/plaque.png": "ENDPLAK.png",
    "img/icons/tent.png": "ICONS/0003.png",
    "img/icons/castle.png": "ICONS/0000.png",
    "img/icons/cave.png": "ICONS/0010.png",
    "img/icons/hills.png": "ICONS/0011.png",
    "img/icons/compass.png": "COMPASS/0000.png",
}

# The game's dialog boxes are drawn from 16x16 tiles, nine per style:
# fill, four corners, then the top, right, bottom and left edges.
FRAME_STYLES = {
    "img/frames/knot.png": 9,
    "img/frames/stone.png": 18,
}
FRAME_TILE = 16
FRAME_SCALE = 2
SPRITE_SCALE = 3  # Overworld sprites are tiny; enlarge them, keeping hard pixels.

# The fully grown Mana Dome of each colour, in SPR/DOMES1-5/.
MANA_DOME_FRAMES = {"red": "0003", "blue": "0007", "black": "0011", "green": "0015", "white": "0019"}

PARCHMENT_SOURCE = "DuelArt/GAUN_Startup.png"
PARCHMENT_CROP = (16, 16, 534, 393)  # Trim the bevelled edge of the 550x409 panel.


def publish_assets(
    converted: Path, out: Path, cards: list[Card], creatures: list[Creature]
) -> None:
    for published, source in GAME_ART.items():
        save_image(converted / source, out / published)

    for lord in GUILD_LORDS:
        color = lord.color.upper()
        save_image(converted / f"DuelArt/LIFE_{color}pict.png", out / lord.portrait)
        save_without_black(
            converted / f"DuelArt/QUESTMANA_{lord.color.capitalize()}.png", out / lord.orb
        )

    for published, first_tile in FRAME_STYLES.items():
        build_frame(converted / "DBOX", first_tile, out / published)

    parchment = Image.open(converted / PARCHMENT_SOURCE).crop(PARCHMENT_CROP)
    parchment.save(out / "img/parchment.webp", quality=85)

    for frame in {card.frame for card in cards}:
        save_image(
            converted / f"CardArt/CARDBK_{frame}.png", out / f"img/frames/card-{frame}.webp"
        )

    # Converting ~400 illustrations is the slow part of a build, so reuse the
    # ones already converted. Each file is named after its source, so a stale
    # copy can only come from changed game art: delete _site/ to rebuild then.
    for card in cards:
        dest = out / f"img/cards/{card.art}.webp"
        if not dest.exists():
            save_image(converted / f"CardArt/medart/{card.art}.png", dest)

    for place in PLACES:
        save_image(converted / f"ICONS/{place.icon}.png", out / place.image)

    for terrain in TERRAINS:
        frame = MANA_DOME_FRAMES[terrain.color]
        save_sprite(converted / f"SPR/DOMES1-5/{frame}.png", out / terrain.mana_dome)

    for creature in creatures:
        # Frame 0 of each walking animation faces the viewer.
        save_sprite(converted / f"SPR/{creature.sprite}/0000.png", out / creature.image)

    shutil.copytree(converted / "fonts", out / "fonts", dirs_exist_ok=True)


def save_image(source: Path, dest: Path) -> None:
    """Copy a PNG, or convert it when the destination ends in .webp."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix == ".webp":
        Image.open(source).save(dest, quality=85, method=6)
    else:
        shutil.copyfile(source, dest)


def save_sprite(source: Path, dest: Path) -> None:
    """Crop a sprite to its figure and enlarge it with nearest-neighbour scaling."""
    sprite = Image.open(source).convert("RGBA")
    sprite = sprite.crop(sprite.getbbox())
    size = (sprite.width * SPRITE_SCALE, sprite.height * SPRITE_SCALE)
    dest.parent.mkdir(parents=True, exist_ok=True)
    sprite.resize(size, Image.Resampling.NEAREST).save(dest)


def save_without_black(source: Path, dest: Path) -> None:
    """Save a sprite with its pure black background made transparent."""
    image = Image.open(source).convert("RGBA")
    image.putdata([(0, 0, 0, 0) if pixel[:3] == (0, 0, 0) else pixel for pixel in image.getdata()])
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)


def build_frame(tiles: Path, first_tile: int, dest: Path) -> None:
    """Join nine dialog tiles into one image for CSS border-image."""
    fill, top_left, top_right, bottom_left, bottom_right, top, right, bottom, left = (
        Image.open(tiles / f"{first_tile + offset:04d}.png").convert("RGBA")
        for offset in range(9)
    )
    layout = [
        [top_left, top, top_right],
        [left, fill, right],
        [bottom_left, bottom, bottom_right],
    ]
    frame = Image.new("RGBA", (FRAME_TILE * 3, FRAME_TILE * 3))
    for row, tiles_in_row in enumerate(layout):
        for column, tile in enumerate(tiles_in_row):
            frame.paste(tile, (column * FRAME_TILE, row * FRAME_TILE))

    size = FRAME_TILE * 3 * FRAME_SCALE
    dest.parent.mkdir(parents=True, exist_ok=True)
    frame.resize((size, size), Image.Resampling.NEAREST).save(dest)
