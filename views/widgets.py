from PyQt5.QtWidgets import (
    QGroupBox,
    QLineEdit,
)

class ReadOnlyLine(QLineEdit):
    'A read-only `QLineEdit`.'
    def __init__(self, value):
        super().__init__(value)
        self.setReadOnly(True)

class TabGroupBox(QGroupBox):
    'Wraps a layout with a `QGroupBox`. Useful to surround elements in tab panes.'
    def __init__(self, layout):
        super().__init__()
        self.setLayout(layout)
