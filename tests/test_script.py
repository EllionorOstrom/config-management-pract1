"""Tests for the start script and command line parameters."""

import io
import os
import tempfile
import unittest

from src.emulator import build_arg_parser
from src.shell import Shell


class ScriptTests(unittest.TestCase):
    """Stage 2: start script execution."""

    def setUp(self):
        """Create a shell writing to a buffer."""
        self.out = io.StringIO()
        self.shell = Shell(out=self.out)
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def make_script(self, text):
        """Write a script file and return its path."""
        path = os.path.join(self.folder.name, "start.emu")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
        return path

    def test_input_and_output_are_shown(self):
        """The dialogue contains both the command and its result."""
        path = self.make_script("ls a\n")
        self.assertTrue(self.shell.run_script(path))
        output = self.out.getvalue()
        self.assertIn("ls a", output)
        self.assertIn("ls ['a']", output)

    def test_comments_are_not_executed(self):
        """Comment lines are shown but not run."""
        path = self.make_script("# ls hidden\n")
        self.shell.run_script(path)
        self.assertNotIn("['hidden']", self.out.getvalue())

    def test_errors_do_not_stop_script(self):
        """A failing line does not prevent the next ones."""
        path = self.make_script("foo\nls ok\n")
        self.shell.run_script(path)
        self.assertIn("command not found", self.out.getvalue())
        self.assertIn("ls ['ok']", self.out.getvalue())

    def test_exit_stops_script(self):
        """Lines after exit are not executed."""
        path = self.make_script("exit\nls after\n")
        self.shell.run_script(path)
        self.assertNotIn("['after']", self.out.getvalue())

    def test_missing_script(self):
        """A missing script is reported."""
        result = self.shell.run_script("no_such_file.emu")
        self.assertFalse(result)
        self.assertIn("script error", self.out.getvalue())


class ArgumentTests(unittest.TestCase):
    """Stage 2: command line parameters."""

    def test_both_parameters(self):
        """Both parameters are parsed."""
        args = build_arg_parser().parse_args(
            ["--vfs", "a.zip", "--script", "s.emu"]
        )
        self.assertEqual(args.vfs, "a.zip")
        self.assertEqual(args.script, "s.emu")

    def test_defaults(self):
        """Parameters are optional."""
        args = build_arg_parser().parse_args([])
        self.assertIsNone(args.vfs)
        self.assertIsNone(args.script)


if __name__ == "__main__":
    unittest.main()
