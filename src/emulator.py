"""Entry point of the shell emulator."""

import argparse
import sys

from src.shell import Shell

EXIT_OK = 0
EXIT_ERROR = 1
NOT_SET = "(not set)"


def build_arg_parser():
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="emulator",
        description="UNIX-like shell emulator.",
    )
    parser.add_argument(
        "--vfs",
        metavar="PATH",
        help="path to the physical location of the VFS",
    )
    parser.add_argument(
        "--script",
        metavar="PATH",
        help="path to the start script with emulator commands",
    )
    return parser


def print_debug(args):
    """Print all parameters given at start-up."""
    print("[debug] start-up parameters:")
    print(f"[debug]   vfs    = {args.vfs or NOT_SET}")
    print(f"[debug]   script = {args.script or NOT_SET}")


def main(argv=None):
    """Run the emulator and return the process exit code."""
    args = build_arg_parser().parse_args(argv)
    print_debug(args)
    shell = Shell()
    if args.script and not shell.run_script(args.script):
        return EXIT_ERROR
    if shell.running:
        shell.run_interactive()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
