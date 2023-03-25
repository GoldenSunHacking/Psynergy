from typing import cast

from PyQt5.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
)

from data.rom_loader import Rom

from .state import state
from .widgets import ReadOnlyLine

class RomInfoTab(QGroupBox):
    'Displays some basic information about the loaded ROM.'
    def __init__(self):
        super().__init__()

        loaded_rom = cast(Rom, state.loadedRom)
        pathLine    = ReadOnlyLine(loaded_rom.file_path)
        nameLine    = ReadOnlyLine(loaded_rom.game_name)
        intNameLine = ReadOnlyLine(loaded_rom.game_internal_name)
        gameIdLine  = ReadOnlyLine(loaded_rom.game_id)
        sizeLine    = ReadOnlyLine(str(len(loaded_rom.rom_binary_data)))
        crc32Line   = ReadOnlyLine(loaded_rom.crc32)

        layout = QGridLayout()

        layout.addWidget(QLabel('Path:'),      0, 0)
        layout.addWidget(pathLine,             0, 1)

        # TODO add icon for game
        layout.addWidget(QLabel('Game Name:'), 1, 0)
        layout.addWidget(nameLine,             1, 1)

        layout.addWidget(QLabel('Int Name:'),  2, 0)
        layout.addWidget(intNameLine,          2, 1)

        layout.addWidget(QLabel('Game ID:'),   3, 0)
        layout.addWidget(gameIdLine,           3, 1)

        layout.addWidget(QLabel('File Size:'), 4, 0)
        layout.addWidget(sizeLine,             4, 1)

        # TODO highlight and warn when this CRC doesn't match the vanilla CRC
        layout.addWidget(QLabel('CRC32:'),     5, 0)
        layout.addWidget(crc32Line,            5, 1)

        self.setLayout(layout)
