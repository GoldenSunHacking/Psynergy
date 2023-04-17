'''
Golden Sun compresses its text using a compression scheme that's basically
indecipherable to mere mortals.

GitHub user "romhack" is a demigod that figured out this compression, wrote
a working decompressor, documented their findings, AND uploaded it all to
GitHub: https://github.com/GoldenSunHacking/GoldenSunCompression.

The following is my attempt to summarize this info, so the code makes sense:

Text is compressed using "modified Huffman" (See:
https://en.wikipedia.org/wiki/Huffman_coding). Instead of one big tree, each
character has its own smaller tree. Whatever the last character read was, that
character's tree is used to determine the next character in the string. Every
string encoding starts from the "null tree", aka the tree for `\0`.

Text data is made up of 4 parts, laid out in the following order:
1. Character Tree Block
2. Character Offset Pointer Table
3. Character Data Pointer Pair
4. Compressed Text Data Blocks
5. Text Block Pointer Table


1. Character Tree Block:

As mentioned before, each character has its own Huffman tree for determining
the next character. This is where those trees are stored. Each tree is preceded
by a char lookup table. This char lookup table is stored in reverse order
(this will make more sense later). The data is laid out like this:
[char 0 lookup][char 0 tree][char 1 lookup][char 1 tree][char 2...]
NOTE: This means each tree and its lookup table will have a different length!

When you traverse a char tree, the bits that make up the traversal give you an
integer. This integer is used as an index into the tree's character lookup
table to get the matching character (i.e. the next character in the string).
NOTE: Each character in this lookup table is encoded using 12 bits!

If a character never appears in the game's script (such as "^"), it will not
have any data at all in this block.

TODO how do we know when we've reached a leaf in the tree?

Characters in this block are in order corresponding to their numeric code.
For English, this is ASCII order.

2. Character Offset Pointer Table

Since each character's tree block can be a different size (and non-occurring
chars are skipped entirely), we can't just index into the tree block.
That's where this table comes in. This is a table of 16 bit pointers that point
at each character's tree. Like the character trees, the order of the pointers
in this table corresponds to the character's numeric code. This table has a
fixed size, so we can index into it as a proxy for the tree block.

These pointers are relative to the beginning of the character tree block,
hence "offset pointer". To get the absolute address they refer to, you do
`[start of char tree block pointer] + [offset pointer]`.

NOTE: there are two special pointer values to look out for:
0x8000 - A dummy pointer that indicates the character has no tree data.
0x0    - Padding at the end of the table
        (presumably to align the bytes for the Char Data Pointer Pair).

These pointers point to the address between the character's lookup table and
its tree. Remember, the character lookup table is reversed, so this address is
pointing to the beginning of the tree *and* the lookup table.
The pointer pulls double duty.

Using the example from part 1: X, Y, and Z are pointers in this table.
[char 0 lookup]X[char 0 tree][char 1 lookup]Y[char 1 tree][char 2...]Z

NOTE: there is some ambiguity about where a character's tree data ends and the
following character's lookup data begins. We use a shortcut to work this out.
Starting at a character's given pointer, we read the lookup table data
char-by-char until we read a non-char value, then assume that's the end of the
table (and thus, the end of the previous char's tree data).
There may be a smarter way to do this, but this works for now.

3. Character Data Pointer Pair

This is two sequential 32-bit pointers.
The first points at the start of the character tree block.
The second points at the start of the offset pointer table.

TODO what points at this address pair?

4. Compressed Text Data Blocks

The compressed text data starts at the address immediately following the
main char pointer pair.

TODO haven't gotten here yet, need to actually decode something successfully first.
TODO discuss blocks
    - block of text data
    - length table for text data

5. Text Block Pointer Table

TODO haven't gotten here yet. Describe this better.
block of 2 pointer structs.
both pointers are 32 bit.
first pointer to start of block's text
second pointer to start of length table
TODO what points at this?


The 500 IQ sage who came up with this one must have been doing coke with Jesus.
'''

from itertools import filterfalse
from math import ceil
from typing import Iterator, List

#from dahuffman import HuffmanCodec
from more_itertools import pairwise


from rom_data import RomData

# Some discussion on memory positions for text reading
#https://discord.com/channels/243488870962823200/332622755419652096/1093661000550592593


# TODO Put the char trees through HuffmanCodec and see if the binary matches.
# If so, we can leverage that library.

# TODO better name for this. This is where the game programming stops
# and game data begins, so data pointers are relative to this.
ROM_OFFSET = 0x08_00_00_00

NO_CHAR_OFFSET = 0x8000
'Dummy offset used when a character has no tree.'

class CharPointerPair:
    'Accessor over `RomData` for a character data pointer pair.'

    # TODO it would be nice to have a better detection mechanism for this address
    # rather than just hard-coding it for each game. A signature or something.
    def __init__(self, romData: RomData, address: int):
        self._address = address
        self._romData = romData

    def getPairAddress(self) -> int:
        'Returns the pointer to this pointer pair.'
        return self._address

    def getTreeBlockAddress(self) -> int:
        'Returns the pointer to the start of the character tree block.'
        return self._romData.getInt32(self._address) - ROM_OFFSET

    def getLookupTableAddress(self) -> int:
        'Returns the pointer to the start of the character offset pointer table.'
        return self._romData.getInt32(self._address + 4) - ROM_OFFSET

    def __str__(self) -> str:
        return f'''{CharPointerPair.__name__}({hex(self.getPairAddress())} -> [{
            hex(self.getTreeBlockAddress())
        }, {
            hex(self.getLookupTableAddress())
        }])'''

class CharTree:
    '''The loaded data for a single Huffman character tree.

    NOTE: Not an accessor over `RomData`.
    '''

    @staticmethod
    def isValidChar(char: int) -> bool:
        'Returns whether or not the given char code corresponds to a valid character.'
        # TODO this needs updated to support other languages.
        return 0x00 < char < 0x7E

    def __init__(self, char: str, offset: int):
        self._char = char
        self._lookupTable: 'List[str]|None' = None
        self._treeData: 'RomData|None' = None

        # I don't love storing this value since it directly depends on the
        # underlying memory, but it makes memory actions much simpler
        # in CharTreeBlock.
        self._offset = offset

    def empty(self) -> bool:
        'Returns whether or not this is an empty tree (i.e. no character data).'
        return self._lookupTable is None and self._treeData is None

    def loadLookupTable(self, romData: RomData, startAddress: int):
        '''Reads characters from `romData` starting at `startAddress`
        into the char lookup table.'''
        self._lookupTable = []

        # startAddress is the start of the TREE data.
        # The previous byte is the start of the lookup table.
        for addr in range(startAddress - 1, 0, -3):
            # Remember, these are 12-bit chars and this table is reversed.
            partA = romData.getInt8(addr - 0)
            partB = romData.getInt8(addr - 1)
            partC = romData.getInt8(addr - 2)

            char1 = (partA << 4) | (partB >> 4)
            char2 = ((partB & 0xF) << 8) | partC

            # There may be a smarter way to figure out the length of the
            # lookup table, but we're just going to read characters until we
            # see garbage, then assume that's the end.
            if CharTree.isValidChar(char1):
                self._lookupTable.append(chr(char1))
            else:
                break

            if CharTree.isValidChar(char2):
                self._lookupTable.append(chr(char2))
            else:
                break

    def loadTreeData(self, romData: RomData, startAddress: int, endAddress: int):
        'Reads the `romData` from `startAddress` to `endAddress` as a tree.'
        self._treeData = romData.getSliceRange(startAddress, endAddress)

    def sizeLookup(self) -> int:
        '''Returns the size of the character lookup table, in bytes.

        Characters are encoded using 12-bits, so this value will be larger
        than the length of the lookup table.
        '''
        if self._lookupTable is None:
            raise Exception('Char lookup table not loaded yet!')
        return ceil((len(self._lookupTable) * 12) / 8)

    def sizeTree(self) -> int:
        'Returns the size of the tree data, in bytes.'
        if self._treeData is None:
            raise Exception('Tree data not loaded yet!')
        return len(self._treeData)

    def __str__(self) -> str:
        return f'{CharTree.__name__}({repr(self._char)}, {self._lookupTable})'

class CharTreeBlock:
    'An accessor over `RomData` for reading Huffman character tree blocks.'
    def __init__(self, romData: RomData, charPtrs: CharPointerPair):
        self._romData = romData
        self._charTrees: List[CharTree] = []

        self._loadCharLookupTables(charPtrs)
        self._loadCharTrees(charPtrs)

    def _loadCharLookupTables(self, charPtrs: CharPointerPair):
        'Reads in character lookup tables for each char in the offset table.'
        treeBlockStartAddress = charPtrs.getTreeBlockAddress()
        lookupStartAddress = charPtrs.getLookupTableAddress()
        lookupEndAddress = charPtrs.getPairAddress()

        # Iterate through the table of 16-bit address offsets for each char.
        for charCode, ptrOffsetAddress in enumerate(range(lookupStartAddress, lookupEndAddress, 2)):
            offset = self._romData.getInt16(ptrOffsetAddress)

            if offset == 0x0:
                # Load complete, we've reached the end-of-table padding.
                return

            charTree = CharTree(chr(charCode), offset)

            if offset != NO_CHAR_OFFSET:
                charTreeAddress = treeBlockStartAddress + offset
                charTree.loadLookupTable(self._romData, charTreeAddress)

            self._charTrees.append(charTree)

    def _loadCharTrees(self, charPtrs: CharPointerPair):
        '''Reads in character tree data.

        This assumes a char tree ends where the next char's lookup table
        begins, so this requires all char tree lookup tables have already
        been read in.
        '''
        treeBlockStartAddress = charPtrs.getTreeBlockAddress()

        # Empty trees don't appear in the data at all.
        nonEmptyTrees = filterfalse(CharTree.empty, self._charTrees)
        for prevTree, curTree in pairwise(nonEmptyTrees):
            prevTree.loadTreeData(
                romData=self._romData,
                startAddress=(treeBlockStartAddress + prevTree._offset),
                endAddress=(treeBlockStartAddress + curTree._offset - curTree.sizeLookup()),
            )

        # Last tree ends where lookup table begins.
        # Python weirdness: curTree is still set from above for loop.
        curTree.loadTreeData(
            romData=self._romData,
            startAddress=(treeBlockStartAddress + curTree._offset),
            endAddress=(charPtrs.getLookupTableAddress() - 1),
        )

    def __getitem__(self, key: 'str|int') -> CharTree:
        if isinstance(key, str):
            if len(key) > 1:
                raise KeyError('Only single-char keys are allowed')
            key = ord(key)
        return self._charTrees[key]

    # TODO might make sense to subclass dict so we get things like .items()
    def __iter__(self) -> Iterator[CharTree]:
        return iter(self._charTrees)

    def __str__(self) -> str:
        return f'{CharTreeBlock.__name__}({{\n' + \
            '\n'.join(map(lambda tree: f'\t{tree}', self._charTrees)) + \
            '\n})'


# Local test. Load a rom file and get strings out of it.
if __name__ == '__main__':
    from sys import argv, exit

    data = RomData.fromFile(argv[1])
    pair = CharPointerPair(data, 0x3842c)
    print(pair)
    trees = CharTreeBlock(data, pair)
    print('TREE BLOCK START', hex(pair.getTreeBlockAddress()))
    for tree in trees:
        if tree.empty():
            print(f'Tree {repr(tree._char).rjust(6)}, [None, None, None]')
            continue
        blockStart = pair.getTreeBlockAddress()
        charStart = blockStart + tree._offset
        lookupEnd = blockStart + tree._offset - tree.sizeLookup()
        treeEnd = blockStart + tree._offset + tree.sizeTree()
        print(f'Tree {repr(tree._char).rjust(6)} [{hex(lookupEnd)}, {hex(charStart)}, {hex(treeEnd)}] [{tree.sizeLookup()}, {tree.sizeTree()}]')