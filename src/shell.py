"""Shell emulator: prompt, command dispatch and commands."""

import getpass
import socket
import sys

from src.cmdparser import ParseError, parse

NO_ARGS = 0
MAX_CD_ARGS = 1
COMMENT_MARK = "#"
SCRIPT_ENCODING = "utf-8-sig"


class ShellError(Exception):
    """Raised by a command; the message is shown to the user."""


class Shell:
    """Emulator of a UNIX-like command line."""

    def __init__(self, out=None):
        """Create a shell that prints to ``out`` (stdout by default)."""
        self.out = out if out is not None else sys.stdout
        self.running = True
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

    def write(self, text):
        """Print a line of output."""
        print(text, file=self.out)

    def prompt(self):
        """Build the prompt from real OS data: user@host:~$ ."""
        return f"{getpass.getuser()}@{socket.gethostname()}:~$ "

    def execute(self, line):
        """Parse and run one command line, reporting errors."""
        try:
            tokens = parse(line)
        except ParseError as error:
            self.write(f"parse error: {error}")
            return
        if tokens:
            self._run_command(tokens[0], tokens[1:])

    def _run_command(self, name, args):
        """Find a command by name and run it."""
        handler = self.commands.get(name)
        if handler is None:
            self.write(f"{name}: command not found")
            return
        try:
            handler(args)
        except ShellError as error:
            self.write(f"{name}: {error}")

    def run_interactive(self):
        """Read and execute commands until exit or end of input."""
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                self.write("")
                break
            except KeyboardInterrupt:
                self.write("")
                continue
            self.execute(line)

    def run_script(self, path):
        """Run a start script, echoing both input and output.

        Returns False if the script file cannot be read.
        """
        try:
            with open(path, encoding=SCRIPT_ENCODING) as file:
                lines = file.read().splitlines()
        except (OSError, UnicodeDecodeError) as error:
            self.write(f"script error: cannot read {path}: {error}")
            return False
        for line in lines:
            if not self.running:
                break
            self._run_script_line(line)
        return True

    def _run_script_line(self, line):
        """Show one script line as typed input and run it."""
        if not line.strip():
            return
        self.write(self.prompt() + line)
        if not line.strip().startswith(COMMENT_MARK):
            self.execute(line)

    @staticmethod
    def _check_args(args, limit):
        """Raise ShellError if there are more than ``limit`` arguments."""
        if len(args) > limit:
            raise ShellError("too many arguments")

    def cmd_ls(self, args):
        """Stub: print the command name and its arguments."""
        self.write(f"ls {args}")

    def cmd_cd(self, args):
        """Stub: print the command name and its arguments."""
        self._check_args(args, MAX_CD_ARGS)
        self.write(f"cd {args}")

    def cmd_exit(self, args):
        """Leave the shell."""
        self._check_args(args, NO_ARGS)
        self.running = False
