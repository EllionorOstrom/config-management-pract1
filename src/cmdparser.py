"""Parser of command lines with support for quoted arguments."""

import os

QUOTES = "'\""


class ParseError(Exception):
    """Raised when a command line cannot be parsed."""


class _Scanner:
    """Character-by-character tokenizer state."""

    def __init__(self):
        """Create an empty scanner."""
        self.tokens = []
        self.chars = []
        self.in_token = False
        self.quote = None

    def feed(self, char):
        """Process the next character of the line."""
        if self.quote:
            self._feed_quoted(char)
        elif char in QUOTES:
            self.quote = char
            self.in_token = True
        elif char.isspace():
            self.flush()
        else:
            self.chars.append(char)
            self.in_token = True

    def _feed_quoted(self, char):
        """Process a character inside quotes."""
        if char == self.quote:
            self.quote = None
        else:
            self.chars.append(char)

    def flush(self):
        """Finish the current token if there is one."""
        if self.in_token:
            self.tokens.append("".join(self.chars))
            self.chars = []
            self.in_token = False


def parse(line):
    """Split a line into tokens.

    Spaces separate tokens, except inside single or double quotes.
    Environment variables (like $HOME) are expanded.
    Raises ParseError if a quote is not closed.
    """
    scanner = _Scanner()
    for char in line:
        scanner.feed(char)
    if scanner.quote:
        raise ParseError(f"unclosed quote {scanner.quote}")
    scanner.flush()
    return [os.path.expandvars(token) for token in scanner.tokens]