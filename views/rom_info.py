from typing import cast, Optional

from PyQt5.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QWidget,
)

from .state import state
from .widgets import ReadOnlyLine

class RomInfoTab(QGroupBox):
    'Displays some basic information about the loaded ROM.'
    def __init__(self, parent: Optional[QWidget]=None):
        super().__init__(parent)

        loadedRom = state.loadedRom
        if loadedRom is None:
            raise Exception('RomInfoTab instantiated without ROM loaded.')

        pathLine    = ReadOnlyLine(loadedRom.filePath())
        nameLine    = ReadOnlyLine(loadedRom.gameName())
        intNameLine = ReadOnlyLine(loadedRom.header().internalName())
        gameIdLine  = ReadOnlyLine(loadedRom.header().fullGameId())
        sizeLine    = ReadOnlyLine(str(loadedRom.data().size()))
        crc32Line   = ReadOnlyLine(loadedRom.data().crc32())

        layout = QGridLayout(self)

        layout.addWidget(self._label('Path:'),      0, 0)
        layout.addWidget(pathLine,                  0, 1)

        # TODO add icon for game
        layout.addWidget(self._label('Game Name:'), 1, 0)
        layout.addWidget(nameLine,                  1, 1)

        layout.addWidget(self._label('Int Name:'),  2, 0)
        layout.addWidget(intNameLine,               2, 1)

        layout.addWidget(self._label('Game ID:'),   3, 0)
        layout.addWidget(gameIdLine,                3, 1)

        layout.addWidget(self._label('File Size:'), 4, 0)
        layout.addWidget(sizeLine,                  4, 1)

        # TODO highlight and warn when this CRC doesn't match the vanilla CRC
        layout.addWidget(self._label('CRC32:'),     5, 0)
        layout.addWidget(crc32Line,                 5, 1)

        self.setLayout(layout)

    def _label(self, text: str) -> QLabel:
        return QLabel(text, self)