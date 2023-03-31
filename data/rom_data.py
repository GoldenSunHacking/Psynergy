from binascii import crc32
from typing import cast
import struct

class RomData:
    '''Holds the data of a ROM file in a `memoryview`.

    Contains some basic functions for reading and writing arbitrary values
    in the data. Does not enforce any sort of constraints on the data, such
    as invalid memory values.

    All operations are little-endian.
    '''
    def __init__(self, filePath: str):
        self.romFile = filePath
        with open(filePath, 'rb') as romFile:
            self._romData = memoryview(bytearray(romFile.read()))

    def __len__(self):
        return len(self._romData)

    def crc32(self) -> str:
        'The hexadecimal CRC32 hash of the binary data.'
        return hex(crc32(self._romData))[2:]

    def size(self) -> int:
        '''An alias for `len(self)` to avoid that awkward thing where
        everything else uses a function, but size needs `len()`.'''
        return len(self)

    def getInt8(self, index: int) -> int:
        'Reads an 8-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<B', self._romData, index)[0]

    def getInt16(self, index: int) -> int:
        'Reads a 16-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<H', self._romData, index)[0]

    def getInt32(self, index: int) -> int:
        'Reads a 32-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<I', self._romData, index)[0]

    def setInt8(self, index: int, value: int) -> None:
        'Writes an 8-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<B', self._romData, index, value)

    def setInt16(self, index: int, value: int) -> None:
        'Writes a 16-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<H', self._romData, index, value)

    def setInt32(self, index: int, value: int) -> None:
        'Writes a 32-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<I', self._romData, index, value)

    def getAsciiString(self, index: int, length: int) -> str:
        '''Reads a chunk of memory as an ASCII string.
        :raises
            UnicodeDecodeError: if the data isn't a valid ASCII string.
        '''
        return cast(
            bytes,
            struct.unpack_from(f'<{length}s', self._romData, index)[0],
        ).decode('ASCII')

    # NOTE: There is no setAsciiString because it would be a pain in the ass.
