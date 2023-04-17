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

    @staticmethod
    def fromFile(filePath: str) -> 'RomData':
        with open(filePath, 'rb') as romFile:
            romData = memoryview(bytearray(romFile.read()))
        return RomData(romData)

    def __init__(self, romDataView: memoryview):
        self._romDataView = romDataView

    def __getitem__(self, subscript: 'int|slice') -> 'int|RomData':
        '''An accessor for getting single bytes or byte ranges of RomData.
        Slices are wrapped in a new `RomData`
        '''
        if isinstance(subscript, slice):
            return RomData(self._romDataView[subscript])
        else:
            return self._romDataView[subscript]

    def __len__(self):
        return len(self._romDataView)

    def crc32(self) -> str:
        'The hexadecimal CRC32 hash of the binary data.'
        return hex(crc32(self._romDataView))[2:]

    def size(self) -> int:
        '''An alias for `len(self)` to avoid that awkward thing where
        everything else uses a function, but size needs `len()`.'''
        return len(self)

    def getInt8(self, index: int) -> int:
        'Reads an 8-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<B', self._romDataView, index)[0]

    def getInt16(self, index: int) -> int:
        'Reads a 16-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<H', self._romDataView, index)[0]

    def getInt32(self, index: int) -> int:
        'Reads a 32-bit, unsigned, little-endian int from `index`.'
        return struct.unpack_from('<I', self._romDataView, index)[0]

    def setInt8(self, index: int, value: int) -> None:
        'Writes an 8-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<B', self._romDataView, index, value)

    def setInt16(self, index: int, value: int) -> None:
        'Writes a 16-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<H', self._romDataView, index, value)

    def setInt32(self, index: int, value: int) -> None:
        'Writes a 32-bit, unsigned, little-endian int to `index`.'
        struct.pack_into('<I', self._romDataView, index, value)

    def getAsciiString(self, index: int, length: int) -> str:
        '''Reads a chunk of memory as an ASCII string.
        :raises
            UnicodeDecodeError: if the data isn't a valid ASCII string.
        '''
        return cast(
            bytes,
            struct.unpack_from(f'<{length}s', self._romDataView, index)[0],
        ).decode('ASCII')

    # NOTE: There is no setAsciiString because it would be a pain in the ass.

    def getSliceRange(self, start: 'int|None'=None, end: 'int|None'=None) -> 'RomData':
        '''Returns a slice of bytes from address `start` to address `end`.

        This operation is synonymous with `romData[start:end]`.
        '''
        return cast(RomData, self[start:end])
