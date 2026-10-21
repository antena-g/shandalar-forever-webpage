"""Shandalar's lands, places, World Magics and Guild Lords.

Adapted from the 1997 game manual.
"""

from dataclasses import dataclass

MANA_SYMBOLS = {"white": "W", "blue": "U", "black": "B", "red": "R", "green": "G"}


@dataclass(frozen=True)
class GuildLord:
    name: str
    title: str
    color: str
    blurb: str

    @property
    def guild(self) -> str:
        return f"{self.color.capitalize()} Guild"

    @property
    def portrait(self) -> str:
        return f"img/lords/{self.color}.png"

    @property
    def orb(self) -> str:
        return f"img/orbs/{self.color}.png"


GUILD_LORDS = [
    GuildLord(
        name="Alsadim K'mer",
        title="The Sainted One",
        color="white",
        blurb=(
            "Lord of the White Guild, which teaches and polices the magic of the "
            "plains. K'mer bears the post's honorary title."
        ),
    ),
    GuildLord(
        name="Starcryst",
        title="The Astral Visionary",
        color="blue",
        blurb=(
            "She took the name Starcryst when she rose to lead the Blue Guild. "
            "The post has no official title, but few call her anything else."
        ),
    ),
    GuildLord(
        name="Lichlord",
        title="Skavius Slan",
        color="black",
        blurb=(
            "An undead lord in the body of the hero Azaar, the same body Lim-Dul "
            "once wore. He remembers nothing of the life it lived before him."
        ),
    ),
    GuildLord(
        name="Kzzy'n",
        title="The Dragon Lord",
        color="red",
        blurb=(
            "Lord of the Red Guild, which teaches and polices the magic of the "
            "mountains. She bears the post's honorary title."
        ),
    ),
    GuildLord(
        name="The Great Druid",
        title="Lord of the Green Guild",
        color="green",
        blurb=(
            "Lord of the Green Guild, which teaches and polices the magic of the "
            "forests, and known only by the title of the post."
        ),
    ),
]


@dataclass(frozen=True)
class Terrain:
    name: str
    color: str
    land: str  # The basic land card whose art illustrates it.
    description: str

    @property
    def mana_dome(self) -> str:
        return f"img/domes/{self.color}.png"


TERRAINS = [
    Terrain(
        "Plains",
        "white",
        "Plains",
        "The stronghold of white magic. These flat expanses are easy to cross, "
        "for you and for the creatures that live on them.",
    ),
    Terrain(
        "Islands",
        "blue",
        "Island",
        "The coastal lowlands feed blue magic. Splashing through is quicker than "
        "you might think, and the creatures here swim well.",
    ),
    Terrain(
        "Swamps",
        "black",
        "Swamp",
        "Black magic bubbles and slithers in the mire. Slogging through is slow "
        "for travellers, but not for what lives there.",
    ),
    Terrain(
        "Mountains",
        "red",
        "Mountain",
        "The pent-up power of the mountains supplies red magic. Climbing is slow, "
        "and the mountain folk move faster than you.",
    ),
    Terrain(
        "Forests",
        "green",
        "Forest",
        "Green magic lairs in the woods. The undergrowth slows you a little; it "
        "does not slow the denizens of the forest.",
    ),
]


@dataclass(frozen=True)
class Place:
    name: str
    icon: str  # A location illustration from the game's ICONS set.
    description: str

    @property
    def image(self) -> str:
        return f"img/places/{self.icon}.png"


PLACES = [
    Place(
        "Villages",
        "0000",
        "Where most of Shandalar's folk live. Buy and sell cards, stock up on "
        "food, rework your deck, and ask the elders for a quest. Finishing a "
        "quest is the only way to earn a new mana link.",
    ),
    Place(
        "Cities",
        "0005",
        "Fortresses of the minor wizards, who trade rare cards for mana stones. "
        "The Guild Lords covet their power: a conquered city is sealed under a "
        "Mana Dome until you defeat the creature guarding it.",
    ),
    Place(
        "Lairs",
        "0010",
        "Anything that is not a village, city, dungeon or castle is probably a "
        "lair. Inside could be gold, cards, a riddle, a trap, or a great beast "
        "guarding its hoard.",
    ),
    Place(
        "Dungeons",
        "0019",
        "Hidden until a defeated creature tells you where to look. Life lost "
        "carries over from duel to duel, and an enchantment often favours the "
        "dungeon's guardians.",
    ),
    Place(
        "Castles",
        "0007",
        "Each Guild Lord waits in a castle behind their strongest minions. "
        "Bring a deck built against their colour, and every mana link you have.",
    ),
]


@dataclass(frozen=True)
class WorldMagic:
    name: str
    stone: str  # The colour of mana stone it uses up.
    effect: str

    @property
    def stone_symbol(self) -> str:
        return MANA_SYMBOLS[self.stone]


WORLD_MAGICS = [
    WorldMagic("Conjurer's Will", "black", "Edit your deck anywhere, not only in a town."),
    WorldMagic("Quickening", "green", "Travel at twice your normal speed for a while."),
    WorldMagic("Leap of Fate", "blue", "Teleport to any place in Shandalar, explored or not."),
    WorldMagic("Thunder Staff", "red", "Destroy the creature nearest to you, without a duel."),
    WorldMagic(
        "Sword of Resistance",
        "white",
        "Travel to a city under attack and confront the creature besieging it.",
    ),
]
