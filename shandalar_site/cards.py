"""Read the card catalogue (CARDS.DAT) that ships with the 1997 game.

The file starts with two little-endian integers: the number of records and the
size of a string pool. Then come fixed-size records, followed by the pool. Text
fields in a record are offsets into that pool. The offsets below were found by
comparing well-known cards (Air Elemental, Llanowar Elves, Serra Angel, ...).
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from pathlib import Path

from markupsafe import Markup, escape

RECORD_SIZE = 152

# Field offsets inside one record.
NAME = 0x04
COLOR = 0x10
TYPE = 0x14
ART_FILE = 0x4C
RULES = 0x74
FLAVOR = 0x78
POWER = 0x7C
TOUGHNESS = 0x80

# One byte per mana colour; generic mana uses 0x48 to mean "X".
COST_BYTES = {"generic": 0x28, "B": 0x29, "U": 0x2A, "G": 0x2D, "R": 0x2F, "W": 0x30}
X_COST = 0x48

# Power and toughness of 100 or more mean "*"; Angry Mob's 102 is "2+*".
STAR_STAT = 100

COLORS = {
    1: "black",
    2: "blue",
    3: "artifact",
    4: "gold",
    5: "green",
    6: "land",
    7: "red",
    8: "white",
}

CARD_TYPES = {
    1: "Artifact",
    2: "Enchantment",
    3: "Instant",
    4: "Interrupt",
    5: "Land",
    6: "Sorcery",
    7: "Creature",
}

BASIC_LAND_FRAMES = {
    "Plains": "WhiteLand",
    "Island": "BlueLand",
    "Swamp": "BlackLand",
    "Mountain": "RedLand",
    "Forest": "GreenLand",
}

# Position of each symbol in the game's ManaSymbols.png strip (18px each).
MANA_SPRITE_INDEX = {
    "X": 0,
    **{str(number): number + 1 for number in range(11)},
    "W": 12,
    "R": 13,
    "U": 14,
    "B": 15,
    "G": 16,
}

COLOR_ORDER = "WUBRG"


@dataclass(frozen=True)
class Card:
    id: int
    name: str
    color: str
    type: str
    cost: tuple[str, ...]
    rules: str
    flavor: str | None
    power: int
    toughness: int
    art: str

    @property
    def is_creature(self) -> bool:
        return self.type == "Creature" or (self.power, self.toughness) != (0, 0)

    @property
    def stats(self) -> str:
        return f"{_stat_text(self.power)}/{_stat_text(self.toughness)}"

    @property
    def type_line(self) -> str:
        if self.type == "Creature":
            return "Summon Creature"
        if self.type == "Artifact" and self.is_creature:
            return "Artifact Creature"
        return self.type

    @property
    def frame(self) -> str:
        """Name of the card background image in CardArt/."""
        if self.color == "land":
            return BASIC_LAND_FRAMES.get(self.name, "LegendsLand")
        return self.color.capitalize()

    @property
    def text_length(self) -> str:
        """Rough size class, used to shrink long rules text to fit the box."""
        size = len(self.rules)
        if size < 90:
            return "short"
        if size < 180:
            return "medium"
        return "long"


def read_cards(path: Path) -> list[Card]:
    """Return every real card in CARDS.DAT, skipping empty slots and tokens."""
    raw = path.read_bytes()
    count, pool_size = struct.unpack_from("<II", raw)
    pool_start = 8 + count * RECORD_SIZE
    pool = raw[pool_start : pool_start + pool_size]

    def text(offset: int) -> str:
        return pool[offset : pool.index(0, offset)].decode("cp1252")

    cards = []
    for card_id in range(count):
        record = raw[8 + card_id * RECORD_SIZE : 8 + (card_id + 1) * RECORD_SIZE]

        def number(offset: int) -> int:
            return struct.unpack_from("<i", record, offset)[0]

        color = COLORS.get(number(COLOR))
        card_type = CARD_TYPES.get(number(TYPE))
        if color is None or card_type is None:
            continue

        flavor = text(number(FLAVOR))
        cards.append(
            Card(
                id=card_id,
                name=text(number(NAME)),
                color=color,
                type=card_type,
                cost=_read_cost(record),
                rules=text(number(RULES)),
                flavor=None if flavor == "None" else flavor,
                power=number(POWER),
                toughness=number(TOUGHNESS),
                art=Path(text(number(ART_FILE))).stem,
            )
        )
    return cards


def _stat_text(value: int) -> str:
    if value < STAR_STAT:
        return str(value)
    bonus = value - STAR_STAT
    return f"{bonus}+*" if bonus else "*"


def _read_cost(record: bytes) -> tuple[str, ...]:
    generic = record[COST_BYTES["generic"]]
    symbols = []
    if generic == X_COST:
        symbols.append("X")
    elif generic:
        symbols.append(str(generic))
    for color in COLOR_ORDER:
        symbols.extend(color * record[COST_BYTES[color]])
    return tuple(symbols)


def mana_symbol(symbol: str) -> Markup:
    """HTML for one mana symbol, drawn from the game's sprite strip."""
    index = MANA_SPRITE_INDEX.get(symbol)
    if index is None:
        return Markup('<span class="mana mana--text">{}</span>').format(symbol)
    return Markup(
        '<span class="mana" style="--i: {}" role="img" aria-label="{}"></span>'
    ).format(index, symbol)


# In rules text the game writes symbols as "|T", "|R", "|2" and line breaks as "\\".
SYMBOL_PATTERN = re.compile(r"\|(10|[0-9TXWUBRG])")


def rules_to_html(rules: str) -> Markup:
    paragraphs = []
    for paragraph in rules.split("\\\\"):
        parts = SYMBOL_PATTERN.split(str(escape(paragraph.strip())))
        # split() alternates plain text and captured symbols.
        html = "".join(
            _symbol_html(part) if index % 2 else part for index, part in enumerate(parts)
        )
        paragraphs.append(f"<p>{html}</p>")
    return Markup("".join(paragraphs))


def _symbol_html(symbol: str) -> str:
    if symbol == "T":
        return '<span class="tap" role="img" aria-label="tap">t</span>'
    return str(mana_symbol(symbol))
