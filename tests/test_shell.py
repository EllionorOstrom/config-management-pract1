"""Tests for the shell commands."""

import io
import unittest

from src.shell import Shell


class ShellTests(unittest.TestCase):
    """Stage 1: REPL commands and error reporting."""

    def setUp(self):
        """Create a shell writing to a buffer."""
        self.out = io.StringIO()
        self.shell = Shell(out=self.out)

    def run_line(self, line):
        """Execute a line and return everything printed."""
        self.shell.execute(line)
        return self.out.getvalue()

    def test_prompt_format(self):
        """The prompt looks like user@host:~$ ."""
        prompt = self.shell.prompt()
        self.assertIn("@", prompt)
        self.assertTrue(prompt.endswith(":~$ "))

    def test_ls_stub(self):
        """ls prints its name and arguments."""
        self.assertEqual(self.run_line("ls -l 'a b'"), "ls ['-l', 'a b']\n")

    def test_cd_stub(self):
        """cd prints its name and arguments."""
        self.assertEqual(self.run_line("cd /tmp"), "cd ['/tmp']\n")

    def test_unknown_command(self):
        """An unknown command is reported."""
        self.assertIn("command not found", self.run_line("foo"))

    def test_wrong_arguments(self):
        """Too many arguments are reported."""
        self.assertIn("too many arguments", self.run_line("cd a b"))

    def test_parse_error(self):
        """A parse error does not stop the shell."""
        self.assertIn("parse error", self.run_line('ls "x'))
        self.assertTrue(self.shell.running)

    def test_exit(self):
        """exit stops the shell."""
        self.run_line("exit")
        self.assertFalse(self.shell.running)

    def test_exit_with_arguments(self):
        """exit with arguments is an error and does not stop the shell."""
        self.assertIn("too many arguments", self.run_line("exit 1"))
        self.assertTrue(self.shell.running)


if __name__ == "__main__":
    unittest.main()
