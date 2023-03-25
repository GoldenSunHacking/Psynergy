from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
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
        self.keepButton  = self.makeKeepButton()

        self.connectSignals()

        leftColLayout = QVBoxLayout()
        leftColLayout.addWidget(self.searchBar)
        leftColLayout.addWidget(self.stringTable)
        rightColLayout = QVBoxLayout()
        rightColLayout.addWidget(self.previewBox)
        rightColLayout.addWidget(self.editBox)
        rightColLayout.addWidget(self.keepButton)
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

    def makeEditBox(self) -> 'EditBox':
        editBox = EditBox()
        # TODO apply real whitelist for loaded game
        editBox.setWhitelist('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
        editBox.validationFailure.connect(lambda msg: print(msg))
        return editBox

    def makeKeepButton(self) -> QPushButton:
        button = QPushButton('Keep changes')
        button.setDisabled(True)
        return button

    def makePreviewBox(self) -> QTextEdit:
        # TODO make this look like a text box from the game, with the proper font.
        previewBox = QTextEdit()
        previewBox.setDisabled(True)
        previewBox.setReadOnly(True)
        previewBox.setPlaceholderText('In-game preview')
        return previewBox

    def connectSignals(self):
        'Wires widget signals together so they can update each other.'

        # Selecting an item from the table should load it for editing.
        def onItemSelected(itemOpt: Option[StringList.Cell]) -> None:
            self.keepButton.setDisabled(True)
            self.editingItem = itemOpt.getOrRaise()
            self.editBox.setText(self.editingItem.text())
        self.stringTable.selectionModel().selectedItemChanged.connect(onItemSelected)

        # Reflect changes to the edited string in the preview box.
        def onItemEdited() -> None:
            self.previewBox.setText(self.editBox.toPlainText())
            self.keepButton.setDisabled(False)
        self.editBox.textChanged.connect(onItemEdited)

        def onKeepButtonClicked() -> None:
            if self.editingItem is not None:
                self.editingItem.setText(self.editBox.toPlainText())
            self.keepButton.setDisabled(True)
        self.keepButton.clicked.connect(onKeepButtonClicked)


class EditBox(QTextEdit):
    '''A control for editing a game string.

    Entered text can be restricted to a valid character range for the game.
    '''

    validationFailure = pyqtSignal(str)
    'Signal for when an invalid character is entered.'

    # TODO we need a signal for "modified" so modifications can be differentiated from initial loads

    def __init__(self):
        super().__init__()
        self.setAcceptRichText(False)
        self.setDisabled(True)
        self.setPlaceholderText('Select string to edit')

        self._charWhitelist: Optional[str] = None
        self._lastGoodText: Optional[str] = None

        self.textChanged.connect(self._clearInvalidChars)

    def setText(self, text: str) -> None:
        super().setText(text)
        self.setDisabled(False)

    def setWhitelist(self, whitelist: Optional[str]) -> None:
        'Restrict the text area to only accepting characters in the given string.'
        self._charWhitelist = whitelist
        self._lastGoodText = None
        self._clearInvalidChars()

    def _clearInvalidChars(self) -> None:
        # Everything is valid without a whitelist.
        if self._charWhitelist is None:
            return

        # Restore text box to last known good state when an invalid character is entered.
        curText = self.toPlainText()
        badChar = next((char for char in curText if char not in self._charWhitelist), None)
        if badChar is not None:
            if self._lastGoodText is not None:
                self.setText(self._lastGoodText)
                # TODO can we set the cursor to the end of the line?
            self.validationFailure.emit(f'Disallowed character entered: {badChar}')
        else:
            self._lastGoodText = curText
