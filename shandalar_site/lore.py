"""The five Guild Lords of Shandalar, as described in the 1997 game manual."""

from dataclasses import dataclass


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
