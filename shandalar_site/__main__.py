"""Command line: build the site, or build it and serve it locally.

    python -m shandalar_site build
    python -m shandalar_site serve --port 8000
"""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .build import DEFAULT_GAME_ASSETS, WEBSITE, build


def main() -> None:
    parser = argparse.ArgumentParser(prog="shandalar-site", description=__doc__)
    parser.add_argument("command", choices=["build", "serve"])
    parser.add_argument("--out", type=Path, default=WEBSITE / "_site")
    parser.add_argument("--assets", type=Path, default=DEFAULT_GAME_ASSETS)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    build(args.out, args.assets)
    if args.command == "serve":
        serve(args.out, args.port)


def serve(folder: Path, port: int) -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=folder)
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"Serving on http://127.0.0.1:{port}/ (Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
