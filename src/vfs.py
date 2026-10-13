"""In-memory virtual file system loaded from a ZIP archive."""

import base64
import zipfile


class VfsError(Exception):
    """Raised when the VFS cannot be loaded."""


class Node:
    """A file or a directory of the VFS.

    Text files keep their text in ``content``; binary files keep
    base64 text there and have ``binary`` set.
    """

    def __init__(self, name, is_dir, data=b""):
        """Create a node; ``data`` is the raw content of a file."""
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.size = len(data)
        self.binary = False
        self.content = ""
        if not is_dir:
            self._store(data)

    def _store(self, data):
        """Keep data as text, or as base64 if it is not UTF-8 text."""
        try:
            self.content = data.decode("utf-8")
        except UnicodeDecodeError:
            self.binary = True
            self.content = base64.b64encode(data).decode("ascii")


class Vfs:
    """Virtual file system kept entirely in memory."""

    def __init__(self, source=""):
        """Create an empty VFS; ``source`` is its origin for display."""
        self.source = source
        self.root = Node("", True)

    @classmethod
    def from_zip(cls, path):
        """Load a VFS from a ZIP archive, raising VfsError on failure."""
        vfs = cls(path)
        try:
            with zipfile.ZipFile(path) as archive:
                for info in archive.infolist():
                    vfs.add_entry(info.filename, info.is_dir(),
                                  archive, info)
        except FileNotFoundError:
            raise VfsError(f"file not found: {path}") from None
        except zipfile.BadZipFile:
            raise VfsError(f"invalid ZIP format: {path}") from None
        except (OSError, RuntimeError, NotImplementedError) as error:
            raise VfsError(f"cannot read {path}: {error}") from None
        return vfs

    def add_entry(self, name, is_dir, archive, info):
        """Add one archive entry (a file or a directory) to the tree."""
        parts = [part for part in name.replace("\\", "/").split("/")
                 if part]
        if not parts:
            return
        if is_dir:
            self._ensure_dir(parts)
            return
        parent = self._ensure_dir(parts[:-1])
        parent.children[parts[-1]] = Node(
            parts[-1], False, archive.read(info)
        )

    def _ensure_dir(self, parts):
        """Return the directory node for ``parts``, creating it."""
        node = self.root
        for part in parts:
            child = node.children.get(part)
            if child is None:
                child = Node(part, True)
                node.children[part] = child
            elif not child.is_dir:
                raise VfsError(f"conflicting entry: {part}")
            node = child
        return node

    def count(self):
        """Return (number of directories, number of files)."""
        return _count(self.root)

    def tree_lines(self):
        """Return the tree as a list of indented lines."""
        return _tree_lines(self.root, "")


def _count(node):
    """Count directories and files below ``node``."""
    dirs = files = 0
    for child in node.children.values():
        if child.is_dir:
            sub_dirs, sub_files = _count(child)
            dirs += 1 + sub_dirs
            files += sub_files
        else:
            files += 1
    return dirs, files


def _tree_lines(node, prefix):
    """Describe the children of ``node`` as indented lines."""
    lines = []
    for name in sorted(node.children):
        child = node.children[name]
        lines.append(prefix + _describe(child))
        if child.is_dir:
            lines.extend(_tree_lines(child, prefix + "  "))
    return lines


def _describe(node):
    """Return a one-line description of a node."""
    if node.is_dir:
        return node.name + "/"
    kind = "binary" if node.binary else "text"
    return f"{node.name} [{kind}, {node.size} bytes]"
