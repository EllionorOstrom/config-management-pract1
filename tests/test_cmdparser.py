"""Tests for the command line parser."""

import unittest

from src.cmdparser import ParseError, parse


class ParseTests(unittest.TestCase):
    """Parser behaviour."""

    def test_plain_words(self):
        """Words are split by spaces."""
        self.assertEqual(parse("ls -l  /tmp"), ["ls", "-l", "/tmp"])

    def test_empty_line(self):
        """An empty line gives no tokens."""
        self.assertEqual(parse("   "), [])

    def test_double_quotes(self):
        """Double quotes keep spaces inside one argument."""
        self.assertEqual(parse('ls "my dir"'), ["ls", "my dir"])

    def test_single_quotes(self):
        """Single quotes work the same way."""
        self.assertEqual(parse("cd 'a b c'"), ["cd", "a b c"])

    def test_empty_quoted_argument(self):
        """An empty quoted string is an empty argument."""
        self.assertEqual(parse('ls ""'), ["ls", ""])

    def test_glued_quotes(self):
        """Quoted and plain parts glued together form one token."""
        self.assertEqual(parse('ab"c d"e'), ["abc de"])

    def test_other_quote_inside(self):
        """A quote of another kind is a normal character."""
        self.assertEqual(parse("""echo "it's" """), ["echo", "it's"])

    def test_unclosed_quote(self):
        """An unclosed quote is an error."""
        with self.assertRaises(ParseError):
            parse('ls "oops')


if __name__ == "__main__":
    unittest.main()
