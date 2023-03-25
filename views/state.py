from typing import Optional

from data.rom_loader import Rom

class AppState:
    def __init__(self):
        self.loadedRom: Optional[Rom] = None
        self.workingDir: Optional[str] = None

state = AppState()
