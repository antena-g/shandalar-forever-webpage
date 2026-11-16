# Browser development preview — 2026-11-16

The shared menu now links to `try-it-out.html`. The dedicated page retains the
sticky top navigation, frames the game in the site's original-art style, and
loads it only after Launch game. Larger view resizes the existing canvas without
restarting. Startup errors/timeouts expose a retry action. Help text explains
controls, local saves and the current 48/55 encounter scope.

The static build copies the production WASM/JS/snippets plus external portraits,
card art and creature sprites into `_site/game/`. It dereferences the source
`web/assets` symlink so hosting does not depend on the developer's filesystem.
The package is approximately110 MB before HTTP compression; it excludes the
reference executables, raw data and old duel prototype. Most UI art/data are
already embedded in WASM. Normal gameplay does not fetch remote art.

## Verification

- `uv run --locked shandalar-site build`: passes,9 pages/395 gallery cards.
- `uv run python -m unittest discover -s tests -v`:2 tests pass; missing runtime
  fails before publication, symlinked artwork becomes portable regular files.
- `git diff --check`: passes. Workflow YAML parses with PyYAML; the remote GitHub
  Actions workflow was not executed.
- Isolated Chromium with software WebGL2,1440×900: launch, character creation,
  overworld, Beastmaster duel (White/Apprentice, fresh generated campaign),
  concession,35-card campaign save, whole-page reload,
  launch and Resume Game. Art and portraits load from the packaged game folder.
- Standard/larger views preserve the same live canvas; navigation stays at top0.
  Desktop and390×844 page layout have no horizontal page overflow. Mobile game
  play is not certified; the page recommends a desktop mouse/keyboard browser.
- Root-path and `/_site/` subdirectory hosting both launch successfully. Blocking
  the game JS request exposes Try again; unblocking and retrying starts the game.
- No uncaught JavaScript exceptions in the normal browser sessions. Fyrox probes
  optional `.png.options` files, which return404 and use engine defaults; actual
  requested PNG assets load successfully. Firefox/Safari and public hosting were
  not exercised.

Game source: native4cb16c94 / Phase812975f, the previously validated production
browser artifact (no duel-fixtures). No game rules or accepted reference inputs
changed here. Evidence, screenshots and isolated saves are under the parent
`.local/website-browser-preview/`; runtime hashes are in `bundle-hashes.json`.

## Publication

The existing manual GitHub Pages workflow now checks out an explicit game ref,
including Phase, builds the production WASM and packages it with the site. Its
default is the reviewed development version above. Those source commits must be
available on their remotes before running the workflow. No push, workflow run,
release or public deployment was performed as part of this change.

Changed sources: `shandalar_site/build.py`, `shandalar_site/__main__.py`,
`templates/base.html`, `templates/try-it-out.html`, `templates/download.html`,
`static/css/site.css`, `static/js/play.js`, `static/game/index.html`,
`tests/test_browser_bundle.py`, `.github/workflows/deploy.yml`, `.gitignore`,
`README.md` and this report. Generated `_site/` files are intentionally ignored.

## Deployment authentication correction

The first remote attempt failed before compilation because the separate game
checkout used the website-scoped token. The workflow now requires the Actions
secret `GAME_SOURCE_TOKEN` with Contents read access to the game and Phase
repositories, supplies it to recursive checkout, and sets
`persist-credentials: false`. Missing configuration fails with a direct message.
See README.md for exact setup. Local SSH read checks confirm both repository
URLs work; the pinned game/Phase commits are not ancestors of the observed remote
main heads (`6de7cb24` / `ef41efa`). Publishing those commits remains necessary.
No secret was created/read, commits pushed, or remote deployment retried here.
