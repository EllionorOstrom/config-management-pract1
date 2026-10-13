"""Tests for the in-memory VFS loaded from ZIP."""

import io
import os
import tempfile
import unittest
import zipfile

from src.shell import Shell
from src.vfs import Vfs, VfsError

BINARY = bytes([0, 159, 146, 150, 255])


class VfsTests(unittest.TestCase):
    """Stage 3: loading and inspecting the VFS."""

    def setUp(self):
        """Create a temporary folder for archives."""
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def make_zip(self, entries):
        """Create a ZIP archive and return its path."""
        path = os.path.join(self.folder.name, "test.zip")
        with zipfile.ZipFile(path, "w") as archive:
            for name, data in entries.items():
                archive.writestr(name, data)
        return path

    def test_minimal(self):
        """A one-file archive is loaded."""
        vfs = Vfs.from_zip(self.make_zip({"a.txt": b"hi"}))
        self.assertEqual(vfs.count(), (0, 1))
        self.assertEqual(vfs.root.children["a.txt"].content, "hi")

    def test_three_levels(self):
        """Nested directories are created."""
        vfs = Vfs.from_zip(self.make_zip({"a/b/c/d.txt": b"x"}))
        self.assertEqual(vfs.count(), (3, 1))
        self.assertIn("a/", vfs.tree_lines()[0])

    def test_empty_directory_entry(self):
        """Directory entries without files are kept."""
        vfs = Vfs.from_zip(self.make_zip({"empty/": b""}))
        self.assertEqual(vfs.count(), (1, 0))

    def test_binary_is_base64(self):
        """Binary data is stored as base64."""
        vfs = Vfs.from_zip(self.make_zip({"b.bin": BINARY}))
        node = vfs.root.children["b.bin"]
        self.assertTrue(node.binary)
        self.assertEqual(node.content, "AJ+Slv8=")
        self.assertEqual(node.size, len(BINARY))

    def test_file_not_found(self):
        """A missing file is an error."""
        with self.assertRaises(VfsError) as context:
            Vfs.from_zip(os.path.join(self.folder.name, "none.zip"))
        self.assertIn("file not found", str(context.exception))

    def test_invalid_format(self):
        """A file that is not a ZIP is an error."""
        path = os.path.join(self.folder.name, "bad.zip")
        with open(path, "w", encoding="utf-8") as file:
            file.write("not a zip")
        with self.assertRaises(VfsError) as context:
            Vfs.from_zip(path)
        self.assertIn("invalid ZIP format", str(context.exception))

    def test_directory_instead_of_file(self):
        """A directory path is an error, not a crash."""
        with self.assertRaises(VfsError):
            Vfs.from_zip(self.folder.name)

    def test_vfs_info_command(self):
        """vfs-info shows the loaded tree."""
        vfs = Vfs.from_zip(self.make_zip({"d/f.txt": b"x"}))
        out = io.StringIO()
        Shell(out=out, vfs=vfs).execute("vfs-info")
        self.assertIn("directories: 1, files: 1", out.getvalue())
        self.assertIn("f.txt [text, 1 bytes]", out.getvalue())

    def test_vfs_info_without_vfs(self):
        """vfs-info works when no VFS is loaded."""
        out = io.StringIO()
        Shell(out=out).execute("vfs-info")
        self.assertIn("not loaded", out.getvalue())


if __name__ == "__main__":
    unittest.main()
