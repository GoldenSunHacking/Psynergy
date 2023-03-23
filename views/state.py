from typing import Optional

from data.rom_loader import Rom

class AppState:
    def __init__(self):
        self.loaded_rom: Optional[Rom] = None
        self.working_dir: Optional[str] = None

state = AppState()
