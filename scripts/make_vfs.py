"""Generate sample VFS ZIP archives into the ``vfs`` directory.

The archives are not stored in git (see .gitignore); run this
script to create them before testing.
"""

import os
import zipfile

OUTPUT_DIR = "vfs"
BINARY_SAMPLE = bytes([0, 159, 146, 150, 255, 1, 2, 3])

SAMPLES = {
    "minimal.zip": {
        "readme.txt": b"Minimal VFS\n",
    },
    "several.zip": {
        "hello.txt": b"Hello, world!\n",
        "notes.txt": "Notes in UTF-8: \u043f\u0440\u0438\u0432\u0435\u0442\n"
        .encode("utf-8"),
        "empty.txt": b"",
        "data.bin": BINARY_SAMPLE,
    },
    "deep.zip": {
        "docs/readme.txt": b"Docs\n",
        "docs/guide/chapter1/intro.txt": b"Intro\n",
        "docs/guide/chapter1/part/notes.txt": b"Deep notes\n",
        "src/app/main.py": b"print('hi')\n",
        "src/app/utils/helpers.py": b"VALUE = 1\n",
        "empty_dir/": b"",
    },
}


def make_zip(path, entries):
    """Write a ZIP archive with the given {name: bytes} entries."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in entries.items():
            archive.writestr(name, data)


def make_broken(path):
    """Write a file that is not a ZIP archive."""
    with open(path, "w", encoding="utf-8") as file:
        file.write("this is not a zip archive\n")


def main():
    """Create all sample archives."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name, entries in SAMPLES.items():
        make_zip(os.path.join(OUTPUT_DIR, name), entries)
    make_broken(os.path.join(OUTPUT_DIR, "broken.zip"))
    print(f"Sample archives created in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
