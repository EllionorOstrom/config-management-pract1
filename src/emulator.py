"""Entry point of the shell emulator."""

import sys

from src.shell import Shell

EXIT_OK = 0


def main():
    """Run the emulator and return the process exit code."""
    Shell().run_interactive()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
