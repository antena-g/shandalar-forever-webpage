# Shandalar Forever website

A static website for Shandalar Forever, dressed in the art of the 1997 game.

## Build and preview

```sh
uv run shandalar-site serve      # build, then serve on http://127.0.0.1:8000/
uv run shandalar-site build      # only build, into _site/
```

Without uv: `pip install -e .`, then `python -m shandalar_site serve`.

Options: `--out` for the build folder, `--assets` to build from another
folder of game assets instead of `game-assets/`, `--port` for the preview server.

`_site/` is plain static files, so it can be hosted on any static host
(GitHub Pages, Netlify, an nginx folder).

## Where things live

| Path | What it is |
| --- | --- |
| `shandalar_site/build.py` | Renders every page; start reading here |
| `shandalar_site/cards.py` | Reads the game's `CARDS.DAT` card catalogue |
| `shandalar_site/assets.py` | Copies and converts the game art the site uses |
| `shandalar_site/lore.py` | Guild Lords, lands, places and World Magics |
| `shandalar_site/bestiary.py` | Creatures and their decks |
| `shandalar_site/devlog.py` | Loads dev log posts |
| `templates/` | Jinja page templates; `_card.html` draws a card |
| `static/` | Stylesheet and the card archive script |
| `content/devlog/` | Dev log posts in Markdown |
| `content/creatures.csv` | The game's creature table, extracted once from `MAGIC.EXE` |
| `content/screenshots/` | Screenshots of the browser build, listed in `build.py` |
| `game-assets/` | The game files the site uses, copied from the game repository |
| `scripts/sync_game_assets.py` | Refreshes `game-assets/` from `../shandalar-forever/assets/original/` |
| `scripts/extract_creatures.py` | Rebuilds `creatures.csv` from the reference game |

## Writing a dev log post

Add a Markdown file to `content/devlog/`. The file name becomes the URL:

```text
title: Towns open their doors
date: 2026-11-02
summary: One sentence for the post list.
---
The post body, in Markdown.
```

## The look

Nothing comes from a UI kit; the decoration is the game's own art:

- Panels use the game's 16×16 dialog-box tiles, joined into CSS
  `border-image` sprites at build time.
- Buttons use the duel screen's stone button, and headings use its purple
  plaque.
- Cards are drawn on the original card frames, with the original mana
  symbol sprite.
- Fonts are the ones the game shipped: Magic Medieval, Benguiat, Century
  Schoolbook and the symbol font.
