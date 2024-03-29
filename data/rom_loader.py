from dataclasses import dataclass
from typing import Optional

from .rom_data import RomData
from .rom_header import GbaHeader

@dataclass
class RomInfo:
    'Known-good info for a single ROM'
    crc32: str
    'CRC32 hash for this ROM'
    game_id: str
    '4 character identifier for the game. The `XXXX` portion of `AGB-XXXX`.'
    internal_name: str
    '12 character internal name'
    name: str
    'Human-readable name for this ROM. Stolen from mGBA ROM info.'
    size: int
    'File size in bytes'

# Every vanilla ROM I could find for the games we support.
ROM_INFO_MAP = {
    # Golden Sun
    'AGSD': RomInfo(
        name='Golden Sun (Germany)',
        internal_name='GOLDEN_SUN_A',
        game_id='AGSD',
        crc32='1053dce4',
        size=8388608,
    ),
    'AGSE': RomInfo(
        name='Golden Sun (USA, Europe)',
        internal_name='Golden_Sun_A',
        game_id='AGSE',
        crc32='e1fb68e8',
        size=8388608,
    ),
    'AGSF': RomInfo(
        name='Golden Sun (France)',
        internal_name='GOLDEN_SUN_A',
        game_id='AGSF',
        crc32='f6521161',
        size=8388608,
    ),
    'AGSI': RomInfo(
        name='Golden Sun (Italy)',
        internal_name='GOLDEN_SUN_A',
        game_id='AGSI',
        crc32='f3128812',
        size=8388608,
    ),
    'AGSJ': RomInfo(
        name='Ougon no Taiyou - Hirakareshi Fuuin (Japan)',
        internal_name='OugonTaiyo_A',
        game_id='AGSJ',
        crc32='fb96d9de',
        size=8388608,
    ),
    'AGSS': RomInfo(
        name='Golden Sun (Spain)',
        internal_name='GOLDEN_SUN_A',
        game_id='AGSS',
        crc32='c63008d6',
        size=8388608,
    ),

    # Golden Sun: The Lost Age
    'AGFD': RomInfo(
        name='Golden Sun - Die Vergessene Epoche (Germany)',
        internal_name='GOLDEN_SUN_B',
        game_id='AGFD',
        crc32='d981d889',
        size=16777216,
    ),
    'AGFE': RomInfo(
        name='Golden Sun - The Lost Age (USA, Europe)',
        internal_name='GOLDEN_SUN_B',
        game_id='AGFE',
        crc32='606a1c4d',
        size=16777216,
    ),
    'AGFF': RomInfo(
        name="Golden Sun - L'Age Perdu (France)",
        internal_name='GOLDEN_SUN_B',
        game_id='AGFF',
        crc32='1090bd33',
        size=16777216,
    ),
    'AGFI': RomInfo(
        name="Golden Sun - L'Era Perduta (Italy)",
        internal_name='GOLDEN_SUN_B',
        game_id='AGFI',
        crc32='a3e49743',
        size=16777216,
    ),
    'AGFJ': RomInfo(
        name='Ougon no Taiyou - Ushinawareshi Toki (Japan)',
        internal_name='OUGONTAIYO_B',
        game_id='AGFJ',
        crc32='830b795f',
        size=16777216,
    ),
    'AGFS': RomInfo(
        name='Golden Sun - La Edad Perdida (Spain)',
        internal_name='GOLDEN_SUN_B',
        game_id='AGFS',
        crc32='ee38ba94',
        size=16777216,
    ),

    # TODO Golden Sun: Dark Dawn

    # Mario Golf: Advance Tour
    'BMGD': RomInfo(
        name='Mario Golf - Advance Tour (Germany)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGD',
        crc32='3e19e279',
        size=16777216,
    ),
    'BMGE': RomInfo(
        name='Mario Golf - Advance Tour (USA)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGE',
        crc32='d56c2e54',
        size=16777216,
    ),
    'BMGF': RomInfo(
        name='Mario Golf - Advance Tour (France)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGF',
        crc32='bd5be463',
        size=16777216,
    ),
    'BMGI': RomInfo(
        name='Mario Golf - Advance Tour (Italy)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGI',
        crc32='5b0454a',
        size=16777216,
    ),
    'BMGJ': RomInfo(
        name='Mario Golf - GBA Tour (Japan)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGJ',
        crc32='a8342a16',
        size=16777216,
    ),
    'BMGP': RomInfo(
        name='Mario Golf - Advance Tour (Europe)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGP',
        crc32='b483127c',
        size=16777216,
    ),
    'BMGS': RomInfo(
        name='Mario Golf - Advance Tour (Spain)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGS',
        crc32='c35dd9f8',
        size=16777216,
    ),
    'BMGU': RomInfo(
        name='Mario Golf - Advance Tour (Australia)',
        internal_name='MARIOGOLFGBA',
        game_id='BMGU',
        crc32='d6ad422f',
        size=16777216,
    ),

    # Mario Tennis: Power Tour
    'BTME': RomInfo(
        name='Mario Tennis - Power Tour (USA, Australia) (En,Fr,De,Es,It)',
        internal_name='MARIOTENNISA',
        game_id='BTME',
        crc32='da192d29',
        size=16777216,
    ),
    'BTMJ': RomInfo(
        name='Mario Tennis Advance (Japan)',
        internal_name='MARIOTENNISA',
        game_id='BTMJ',
        crc32='975e8d98',
        size=16777216,
    ),
    'BTMP': RomInfo(
        name='Mario Power Tennis (Europe) (En,Fr,De,Es,It)',
        internal_name='MARIOTENNISA',
        game_id='BTMP',
        crc32='c8db4f60',
        size=16777216,
    ),
}

# TODO this is only reaaaaally a GBA Rom. We'll eventually want to differentiate between NDS and GBA
class Rom:
    '''The entry point for reading and manipulating ROM data.
    Contains handles for working with things like ROM headers and string lists.
    '''
    # TODO this might be better in RomInfo
    UNKNOWN_NAME = '<Unknown>'

    def __init__(self, filepath: str):
        self._data = RomData.fromFile(filepath)
        self._filePath = filepath
        self._header = GbaHeader(self._data)

    def data(self) -> RomData:
        'Returns the underlying ROM data.'
        return self._data

    def filePath(self) -> str:
        'Returns the path to the ROM file on disk.'
        return self._filePath

    def header(self) -> GbaHeader:
        return self._header

    # There is no internal human-readable name, so we forward this specific
    # value from RomInfo. All other known-good fields should be read using
    # `matchedInfo().whatever`
    def gameName(self) -> str:
        '''Returns the ROM's human-readable name as reported by mGBA.'''
        info = self.matchedInfo()
        return info.name if info else Rom.UNKNOWN_NAME

    # TODO this is a little odd. This looks up known-good ROM info by game ID,
    # but by accessing it like this, we're sort of implying this data is a
    # property of the loaded ROM, rather than a known-good thing we're supposed
    # to test the ROM against.
    # We could instead ask callers to use RomInfo to take an ID (or even a "Rom")
    def matchedInfo(self) -> Optional[RomInfo]:
        '''Returns the known-good information for this ROM, matched by game ID.
        This infomation is pre-populated, and can be used to validate loaded data.
        '''
        return ROM_INFO_MAP.get(self.header().gameId())
