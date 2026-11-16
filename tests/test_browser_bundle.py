"""The publishable game must survive being moved off the development machine."""
import tempfile
import unittest
from pathlib import Path

from shandalar_site.build import publish_game


class BrowserBundleTests(unittest.TestCase):
    def test_missing_runtime_fails_before_publishing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(FileNotFoundError, "Build the production browser"):
                publish_game(root / "missing", root / "published")
            self.assertFalse((root / "published").exists())

    def test_symlinked_art_is_copied_as_portable_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "web"
            (source / "pkg/snippets").mkdir(parents=True)
            (source / "pkg/shandalar.js").write_text("// runtime")
            (source / "pkg/shandalar_bg.wasm").write_bytes(b"wasm fixture")
            (source / "pkg/snippets/storage.js").write_text("// local saves")
            for folder in ("portraits", "converted/SPR", "converted/CardArt/medart"):
                target = root / "assets/original" / folder
                target.mkdir(parents=True)
                (target / "image.png").write_bytes(b"image fixture")
            (source / "assets").symlink_to(root / "assets", target_is_directory=True)
            output = root / "published"
            publish_game(source, output)
            self.assertFalse(any(path.is_symlink() for path in output.rglob("*")))
            self.assertEqual(
                (output / "game/assets/original/converted/CardArt/medart/image.png").read_bytes(),
                b"image fixture",
            )
            self.assertTrue((output / "game/pkg/snippets/storage.js").is_file())
            self.assertTrue((output / "game/pkg/shandalar_bg.wasm").is_file())


if __name__ == "__main__":
    unittest.main()
