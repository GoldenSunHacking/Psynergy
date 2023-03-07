from PyQt5.QtWidgets import (
    QGroupBox,
    QLineEdit,
)

class ReadOnlyLineEdit(QLineEdit):
    def __init__(self, value):
        super().__init__(value)
        self.setReadOnly(True)

class TabGroupBox(QGroupBox):
    def __init__(self, layout):
        super().__init__()
        self.setLayout(layout)
