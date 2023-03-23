from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from .widgets import StringList

class TextEditTab(QGroupBox):
    '''Displays the list of all strings in the game,
    an editor for modifying them, and a preview for how they'll look in-game.'''

    def __init__(self):
        super().__init__()

        leftColLayout = QVBoxLayout()
        leftColLayout.addWidget(self.makeSearchBar())
        leftColLayout.addWidget(self.makeStringTable())

        rightColLayout = QVBoxLayout()
        rightColLayout.addWidget(self.makePreviewBox())
        rightColLayout.addWidget(self.makeEditBox())

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
        return StringList(items)

    def makePreviewBox(self) -> QTextEdit:
        # TODO make this look like a text box from the game, with the proper font.
        previewBox = QTextEdit()
        previewBox.setReadOnly(True)
        previewBox.setPlaceholderText('In-game preview')
        return previewBox

    def makeEditBox(self) -> QTextEdit:
        editBox = QTextEdit()
        editBox.setPlaceholderText('Select string to edit')
        return editBox
