from typing import List, Tuple

from PySide6 import QtCore, QtGui


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """
    Minimal Python syntax highlighter using Houdini-friendly dark colours.

    Args:
        document (QtGui.QTextDocument): The text document to highlight.
    """

    def __init__(self, document: QtGui.QTextDocument) -> None:
        super().__init__(document)

        self._rules: List[Tuple[QtCore.QRegularExpression, QtGui.QTextCharFormat]] = []

        def add(pattern: str, colour: str, bold: bool = False, italic: bool = False) -> None:
            """
            Helper to add a highlighting rule.

            Args:
                pattern (str): Regex pattern to match.
                colour (str): Hex colour code.
                bold (bool, optional): Whether to make the text bold. Defaults to False.
                italic (bool, optional): Whether to make the text italic. Defaults to False.
            """
            fmt = QtGui.QTextCharFormat()
            fmt.setForeground(QtGui.QColor(colour))
            if bold:
                fmt.setFontWeight(QtGui.QFont.Weight.Bold)
            if italic:
                fmt.setFontItalic(True)
            self._rules.append((QtCore.QRegularExpression(pattern), fmt))

        # Keywords
        # fmt: off
        keywords = [
            "False", "None", "True", "and", "as", "assert", "async", "await", "break",
            "class", "continue", "def", "del", "elif", "else", "except", "finally",
            "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
            "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
        ]
        # fmt: on
        kw_pattern = r"\b(" + "|".join(keywords) + r")\b"
        add(kw_pattern, "#569CD6", bold=True)

        # Built-ins
        # fmt: off
        builtins = [
            "print", "len", "range", "int", "float", "str", "list", "dict", "tuple",
            "set", "bool", "type", "isinstance", "hasattr", "getattr", "setattr",
            "enumerate", "zip", "map", "filter", "sorted", "reversed", "open", "super",
            "self",
        ]
        # fmt: on
        add(r"\b(" + "|".join(builtins) + r")\b", "#DCDCAA")

        # Decorators
        add(r"@\w+", "#C586C0")

        # Numbers
        add(r"\b[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?\b", "#B5CEA8")

        # Double-quoted strings
        add(r'"[^"\\]*(\\.[^"\\]*)*"', "#CE9178")
        # Single-quoted strings
        add(r"'[^'\\]*(\\.[^'\\]*)*'", "#CE9178")

        # Triple-quoted strings (simple, single-line match only)
        add(r'""".*?"""', "#CE9178")
        add(r"'''.*?'''", "#CE9178")

        # Comments
        add(r"#[^\n]*", "#6A9955", italic=True)

        # hou module references
        add(r"\bhou\b", "#4EC9B0", bold=True)

    def highlightBlock(self, text: str) -> None:
        """
        Apply highlighting to a block of text.

        Args:
            text (str): The text block to highlight.
        """
        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)
