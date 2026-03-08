import inspect

import hou
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette


class HoudiniTypeHintPopup(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #555;")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumSize(600, 400)
        self.text_edit.setFont(parent.font())
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def show_hint(self, selected_text, pos):
        """Parse selected text and show type hints"""
        hint = self.get_type_hint(selected_text)
        self.text_edit.setText(hint)
        self.move(pos.x() + 10, pos.y() + 10)
        self.show()

    def set_font(self, font):
        self.text_edit.setFont(font)

    def get_type_hint(self, text):
        """Attempt to resolve and get docstring for selected text"""
        text = text.strip()

        # Try to eval in hou namespace
        try:
            obj = eval(text, {"hou": hou, "__builtins__": __builtins__})
        except:
            return f"Could not resolve: {text}"

        # Try to get signature
        try:
            if callable(obj):
                sig = inspect.signature(obj)
                hint = f"{text}{sig}\n\n"
            else:
                hint = f"{text}: {type(obj).__name__}\n\n"
        except (ValueError, TypeError):
            hint = f"{text}: {type(obj).__name__}\n\n"

        # Get docstring
        doc = inspect.getdoc(obj)
        if doc:
            hint += doc
        else:
            hint += "No documentation available"

        return hint


class HoudiniTextEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.popup = HoudiniTypeHintPopup(self)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        # Show popup on selection
        cursor = self.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            self.popup.show_hint(text, event.globalPos())

    def set_font(self, font):
        self.setFont(font)
        self.popup.set_font(font)
