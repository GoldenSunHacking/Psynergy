from PyQt5.QtWidgets import (
    QLineEdit,
)

class ReadOnlyLine(QLineEdit):
    'A read-only `QLineEdit`.'
    def __init__(self, value):
        super().__init__(value)
        self.setReadOnly(True)
