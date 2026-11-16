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

## Browser development preview

The **try it out** menu opens `try-it-out.html`, with a click-to-launch game
window and a larger view that keeps the site menu visible. The current preview
supports 48 of 55 enemy encounters; saves stay in the browser's local storage.

The site build packages the production game from `../shandalar-forever/web/`.
To refresh that game, run from `../shandalar-forever/`:

```sh
cargo build --locked --release --target wasm32-unknown-unknown --bin shandalar
wasm-bindgen target/wasm32-unknown-unknown/release/shandalar.wasm \
  --out-dir web/pkg --target web
```

Use wasm-bindgen 0.2.129, matching the game's pinned dependency. Do not enable
`duel-fixtures` for the public preview. Then run `uv run shandalar-site build`
in this website directory. `--game-web /path/to/web` selects another prepared
browser build. Missing runtime files stop the build with an actionable error.

Publish the **whole `_site/` directory**, including `game/`. It contains real
copies of the WASM, JavaScript snippets, portraits, creature sprites and card art;
it does not depend on development-machine symlinks or remote artwork. Generated
game files are build output, not tracked source. The game downloads only after
Launch game is pressed. Serve `.wasm` as `application/wasm`; HTTP compression is
recommended for the roughly 54 MB executable. A normal static HTTPS host works;
no backend or account is required. Relative URLs also support a subdirectory.

Use a desktop browser with WebGL 2, a mouse and keyboard. Saves are specific to
the browser and hosting origin; changing the site's domain does not transfer
existing local saves. The page does not publish itself or configure hosting.

The existing manual GitHub Pages workflow now checks out an explicit game commit
(with its Phase submodule), builds WASM without fixtures, and packages it into
the site. Its default is the reviewed November 16 development version. Before
running that remote workflow, the selected game commit and its referenced Phase
commit must exist on their remotes. Local builds do not push or deploy anything.

Packaging checks: `uv run python -m unittest discover -s tests -v`.

### Access to the game repositories in GitHub Actions

The website workflow's default `GITHUB_TOKEN` is scoped to the website repository.
It cannot check out a different private repository, even when both repositories
have the same owner. GitHub reports that as **Repository not found**.

1. Create a fine-grained personal access token with resource owner `antena-g`, selecting
   **only** `shandalar-forever` and `phase-shandalar`, with repository permission
   **Contents: Read-only** (Metadata read access is included automatically).
2. In `shandalar-forever-webpage`, open **Settings → Secrets and variables →
   Actions → New repository secret**. Name it **GAME_SOURCE_TOKEN** and save the
   token there. The workflow uses it for the game checkout and recursive Phase
   submodule, then removes the checkout credentials.
3. Publish the selected Phase commit first, then the game commit that references
   it, and the website workflow change. The selected `game_ref` and its submodule
   commit must exist on GitHub; a token does not upload local commits.
4. Start a **new** Deploy website run using the updated workflow. Re-running an
   old failed run can still use the old workflow definition.

The workflow checks that the secret is configured before attempting the checkout.
If the secret exists but checkout still reports Repository not found, check that
it is unexpired, its owner can read both repositories, both are selected, and any
required organization approval has been granted.

References: [checkout's private-repository instructions](https://github.com/actions/checkout/tree/v5#checkout-multiple-repos-private)
and [GitHub's fine-grained token setup](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
