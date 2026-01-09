import sys

from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo App")

        self.label = QLabel("Not clicked yet")
        self.button = QPushButton("Click me")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Connect button click to handler
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("Button was clicked!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
