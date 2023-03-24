from typing import Optional

from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from data.optional import Option

from .widgets import StringList

class TextEditTab(QGroupBox):
    '''Displays the list of all strings in the game,
    an editor for modifying them, and a preview for how they'll look in-game.'''

    def __init__(self):
        super().__init__()

        self.editingItem: Optional[StringList.Cell] = None

        self.searchBar   = self.makeSearchBar()
        self.stringTable = self.makeStringTable()
        self.editBox     = self.makeEditBox()
        self.previewBox  = self.makePreviewBox()

        self.connectSignals()

        leftColLayout = QVBoxLayout()
        leftColLayout.addWidget(self.searchBar)
        leftColLayout.addWidget(self.stringTable)
        rightColLayout = QVBoxLayout()
        rightColLayout.addWidget(self.previewBox)
        rightColLayout.addWidget(self.editBox)
        paneLayout = QHBoxLayout()
        paneLayout.addLayout(leftColLayout)
        paneLayout.addLayout(rightColLayout)
        self.setLayout(paneLayout)

    def makeSearchBar(self) -> QLineEdit:
        searchBar = QLineEdit()
        searchBar.setPlaceholderText('Search strings')
        return searchBar

    def makeStringTable(self) -> StringList:
        # TODO obviously load real data
        items = ['Test item', 'Something cool here', 'Hi mom'] * 2000
        stringList = StringList(items)
        return stringList

    def makeEditBox(self) -> QTextEdit:
        editBox = QTextEdit()
        editBox.setPlaceholderText('Select string to edit')
        return editBox

    def makePreviewBox(self) -> QTextEdit:
        # TODO make this look like a text box from the game, with the proper font.
        previewBox = QTextEdit()
        previewBox.setReadOnly(True)
        previewBox.setPlaceholderText('In-game preview')
        return previewBox

    def connectSignals(self):
        'Wires widget signals together so they can update each other.'

        # Selecting an item from the table should load it for editing.
        def loadItemForEditing(itemOpt: Option[StringList.Cell]) -> None:
            self.editingItem = itemOpt.getOrRaise()
            self.editBox.setText(self.editingItem.text())
        self.stringTable.selectionModel().selectedItemChanged.connect(loadItemForEditing)

        # Reflect changes to the edited string in the preview box.
        def setPreview() -> None:
            self.previewBox.setText(self.editBox.toPlainText())
        self.editBox.textChanged.connect(setPreview)

