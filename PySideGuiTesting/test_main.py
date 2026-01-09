import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from main import MainWindow


def test_button_click_changes_label(qtbot):
    # Create the window
    window = MainWindow()
    qtbot.addWidget(window)

    # Initially label should be default
    assert window.label.text() == "Not clicked yet"

    # Simulate a user clicking the button
    QTest.mouseClick(window.button, Qt.LeftButton)

    # After click, label should update
    assert window.label.text() == "Button was clicked!"
