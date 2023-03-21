from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QTableView,
    QTextEdit,
    QVBoxLayout,
)

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

    def makeStringTable(self) -> QTableView:
        # TODO obviously load real data
        items = ['Test item', 'Something cool here', 'Hi mom'] * 2000

        listModel = QStandardItemModel()
        listModel.setColumnCount(2)
        listModel.setHorizontalHeaderItem(0, QStandardItem('ID'))
        listModel.setHorizontalHeaderItem(1, QStandardItem('String'))

        for index, string in enumerate(items):
            indexItem = QStandardItem(str(index))
            stringItem = QStandardItem(string)

            indexItem.setEditable(False)
            stringItem.setEditable(False)

            listModel.setItem(index, 0, indexItem)
            listModel.setItem(index, 1, stringItem)

        # TODO make ID column fit contents and be non-resizeable.
        # TODO make string column stretch to fit area.
        tableView = QTableView()
        tableView.setAlternatingRowColors(True)
        tableView.verticalHeader().hide()
        tableView.setModel(listModel)

        return tableView

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
