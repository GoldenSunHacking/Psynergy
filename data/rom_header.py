from .rom_data import RomData

GBA_HEADER_NAME_ADDR = 0xA0
GBA_HEADER_NAME_LEN = 12
GBA_HEADER_ID_ADDR = GBA_HEADER_NAME_ADDR + GBA_HEADER_NAME_LEN
GBA_HEADER_ID_LEN = 4

class GbaHeader:
    'An accessor over `RomData` for reading GBA ROM headers.'
    def __init__(self, romData: RomData):
        self._romData = romData

    def internalName(self) -> str:
        '''Returns the 12-character internal name of the ROM.
        Matches name reported in mGBA.'''
        return self._romData.getAsciiString(GBA_HEADER_NAME_ADDR, GBA_HEADER_NAME_LEN)

    def gameId(self) -> str:
        '''Returns the 4-character game ID of the ROM.
        This is unique to the game version.'''
        return self._romData.getAsciiString(GBA_HEADER_ID_ADDR, GBA_HEADER_ID_LEN)

    def fullGameId(self) -> str:
        'Returns the full game ID as reported by mGBA.'
        return f'AGB-{self.gameId()}'
