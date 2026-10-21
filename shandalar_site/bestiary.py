"""The creatures that roam Shandalar, with the decks they duel with.

content/creatures.csv comes from the game's creature table (see
scripts/extract_creatures.py). Each creature's deck is read from DECKS/ in the
game's raw assets, and card colours come from CARDS.DAT.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .cards import Card
from .lore import MANA_SYMBOLS, TERRAINS

# The Guild Lords wait in their castles and are described on the World page.
GUILD_LORD_TYPES = {7, 14, 21, 28, 35}
NAME_FIXES = {"VampireLord": "Vampire Lord"}

COLOR_ORDER = ["white", "blue", "black", "red", "green"]

# Groups on the Bestiary page: the five terrains, then two extra groups.
HOMELAND_INTROS = {
    **{terrain.name: terrain.description for terrain in TERRAINS},
    "Borderlands": "Where two kinds of land meet, creatures of two colours "
    "roam, and they cross the boundaries without hesitation.",
    "Legends": "The named djinn and dragons of Shandalar, who duel with "
    "decks drawn from three colours.",
}
HOMELANDS = {terrain.color: terrain.name for terrain in TERRAINS}
SIGNATURE_CARD_COUNT = 4


@dataclass(frozen=True)
class DeckCard:
    card: Card
    copies: int


@dataclass(frozen=True)
class Creature:
    type: int
    name: str
    home_colors: tuple[str, ...]
    sprite: str
    deck: tuple[DeckCard, ...]

    @property
    def is_legend(self) -> bool:
        """The named djinn and dragons, who play three-colour decks."""
        return self.type >= 46

    @property
    def homeland(self) -> str:
        if self.is_legend:
            return "Legends"
        if len(self.home_colors) > 1:
            return "Borderlands"
        return HOMELANDS[self.home_colors[0]]

    @property
    def deck_colors(self) -> list[str]:
        """Colours of the spells in the deck, in W, U, B, R, G order."""
        used = {entry.card.color for entry in self.deck}
        for entry in self.deck:
            if entry.card.color == "gold":
                used.update(_colors_in_cost(entry.card))
        return [color for color in COLOR_ORDER if color in used]

    @property
    def mana_symbols(self) -> list[str]:
        return [MANA_SYMBOLS[color] for color in self.deck_colors]

    @property
    def signature_cards(self) -> list[DeckCard]:
        """The spells the creature carries the most copies of."""
        spells = [entry for entry in self.deck if entry.card.type != "Land"]
        return sorted(spells, key=lambda entry: entry.copies, reverse=True)[
            :SIGNATURE_CARD_COUNT
        ]

    @property
    def image(self) -> str:
        return f"img/creatures/{self.sprite}.png"


def load_creatures(table: Path, decks: Path, cards: list[Card]) -> list[Creature]:
    cards_by_id = {card.id: card for card in cards}
    creatures = []
    with table.open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            creature_type = int(row["type"])
            if not row["sprite"] or creature_type in GUILD_LORD_TYPES:
                continue
            creatures.append(
                Creature(
                    type=creature_type,
                    name=NAME_FIXES.get(row["name"], row["name"]),
                    home_colors=tuple(row["home_colors"].split()),
                    sprite=row["sprite"],
                    deck=read_deck(decks / f"{int(row['deck']):04d}.DCK", cards_by_id),
                )
            )
    return creatures


def read_deck(path: Path, cards_by_id: dict[int, Card]) -> tuple[DeckCard, ...]:
    """Read the base deck: one ".<card id> <copies> <name>" line per card.

    Some decks end with ".vBlack", ".vBlue", ... sections: extra cards the
    creature adds against a player of that colour. Only the base deck is read.
    """
    copies = Counter()
    for line in path.read_text(encoding="cp1252").splitlines():
        if line.startswith(".v"):
            break
        if line.startswith("."):
            card_id, count, _name = line[1:].split("\t", maxsplit=2)
            copies[int(card_id)] += int(count)
    return tuple(DeckCard(cards_by_id[card_id], count) for card_id, count in copies.items())


def _colors_in_cost(card: Card) -> set[str]:
    by_symbol = {symbol: color for color, symbol in MANA_SYMBOLS.items()}
    return {by_symbol[symbol] for symbol in card.cost if symbol in by_symbol}


def group_by_homeland(creatures: list[Creature]) -> list[tuple[str, str, list[Creature]]]:
    """(homeland, introduction, creatures) for each group, in page order."""
    return [
        (homeland, intro, [c for c in creatures if c.homeland == homeland])
        for homeland, intro in HOMELAND_INTROS.items()
    ]
