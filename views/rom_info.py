from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
)
from .widgets import ReadOnlyLineEdit, TabGroupBox

def makeRomInfoView():
    # TODO read these values from state
    pathLine    = ReadOnlyLineEdit('')
    nameLine    = ReadOnlyLineEdit('')
    crc32Line   = ReadOnlyLineEdit('')
    gameLine    = ReadOnlyLineEdit('')
    versionLine = ReadOnlyLineEdit('')

    layout = QGridLayout()
    layout.addWidget(QLabel('Path:'),    0, 0)
    layout.addWidget(pathLine,           0, 1)
    layout.addWidget(QLabel('Name:'),    1, 0)
    layout.addWidget(nameLine,           1, 1)
    layout.addWidget(QLabel('Game:'),    2, 0)
    layout.addWidget(gameLine,           2, 1)
    layout.addWidget(QLabel('CRC32:'),   3, 0)
    layout.addWidget(crc32Line,          3, 1)
    layout.addWidget(QLabel('Version:'), 4, 0)
    layout.addWidget(versionLine,        4, 1)

    return TabGroupBox(layout)
