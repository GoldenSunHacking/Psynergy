from data.rom_loader import Rom

class AppState:
    def __init__(self):
        self.loaded_rom: Rom = None
        self.working_dir: str = None

state = AppState()
