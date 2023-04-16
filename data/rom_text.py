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

TODO how do we know when we've reached a leaf in the tree?

Characters in this block are in order corresponding to their numeric code.
For English, this is ASCII order.

2. Character Offset Pointer Table

Since each character's tree block can be a different size, we can't just index
into the tree block. That's where this table comes in. This is a table of
16 bit pointers that point at each character's tree. Like the character trees,
the order of the pointers in this table corresponds to the character's
numeric code. This table has a fixed size, so we can index into it as a proxy
for the tree block.

These pointers are relative to the beginning of the character tree block,
hence "offset pointer". To get the absolute address they refer to, you do
`[start of char tree block pointer] + [offset pointer]`.

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

from typing import Iterator, List

#from dahuffman import HuffmanCodec


from rom_data import RomData

# Some discussion on memory positions for text reading
#https://discord.com/channels/243488870962823200/332622755419652096/1093661000550592593


# TODO Put the char trees through HuffmanCodec and see if the binary matches.
# If so, we can leverage that library.

# TODO better name for this. This is where the game programming stops
# and game data begins, so data pointers are relative to this.
ROM_OFFSET = 0x08_00_00_00

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
    'Accessor over `RomData` for a single Huffman character tree.'

    @staticmethod
    def isValidChar(char: int) -> bool:
        'Returns whether or not the given char code corresponds to a valid character.'
        # TODO this needs updated to support other languages.
        return 0x00 < char < 0x7E

    def __init__(self, romData: RomData, char: str, startAddress: int):
        '''
        romData: The loaded ROM data.

        char: The character this `CharTree` is for.

        startAddress: The start of the tree data.
        NOTE: the start of the lookup table is the byte BEFORE this one.
        '''
        self._char = char
        self._romData = romData
        self._startAddress = startAddress

        self._lookupTable: 'List[str]' = []
        self._treeData: 'RomData|None' = None

        self._loadLookupTable()
        # Can't loadTreeData just yet. We need all the lookup tables first.

    def _loadLookupTable(self):
        'Reads characters from the ROM data into the char lookup table.'
        # _startAddress is the start of the TREE data.
        # The previous byte is the start of the lookup table.
        i = self._startAddress - 1
        while True:
            # Remember, these are 12-bit chars and this table is reversed.
            partA = self._romData.getInt8(i - 0)
            partB = self._romData.getInt8(i - 1)
            partC = self._romData.getInt8(i - 2)
            i -= 3

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

    def loadTreeData(self):
        pass

    def __len__(self) -> int:
        return len(self._lookupTable)

    def __str__(self) -> str:
        return f'{CharTree.__name__}({repr(self._char)}, {self._lookupTable})'

class CharTreeBlock:
    'An accessor over `RomData` for reading Huffman character tree blocks.'
    def __init__(self, romData: RomData, charPtrs: CharPointerPair):
        self._romData = romData
        self._charTrees: List[CharTree] = []

        self._loadCharTrees(charPtrs)

    def _loadCharTrees(self, charPtrs: CharPointerPair):
        startAddress = charPtrs.getLookupTableAddress()
        endAddress = charPtrs.getPairAddress()

        for charCode, ptrAddress in enumerate(range(startAddress, endAddress, 2)):
            charTreeAddress = charPtrs.getTreeBlockAddress() + self._romData.getInt16(ptrAddress)
            self._charTrees.append(CharTree(
                romData      = self._romData,
                char         = chr(charCode),
                startAddress = charTreeAddress,
            ))

    def __getitem__(self, key: 'str|int') -> CharTree:
        if isinstance(key, str):
            if len(key) > 1:
                raise KeyError('Only single-char keys are allowed')
            key = ord(key)
        return self._charTrees[key]

    # TODO might make sense to subclass dict so we get things like .items()
    def __iter__(self) -> Iterator[CharTree]:
        return iter(self._charTrees)

    def __len__(self) -> int:
        return len(self._charTrees)

    def __str__(self) -> str:
        return f'{CharTreeBlock.__name__}({{\n' + \
            '\n'.join(map(lambda tree: f'\t{tree}', self._charTrees)) + \
            '\n})'


# Local test. Load a rom file and get strings out of it.
if __name__ == '__main__':
    from sys import argv, exit

    data = RomData(argv[1])
    pair = CharPointerPair(data, 0x3842c)
    print(pair)
    trees = CharTreeBlock(data, pair)
    print(trees)