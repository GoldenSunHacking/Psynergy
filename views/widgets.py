from typing import cast, List, Optional

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QLineEdit,
    QTableView,
)

from data.optional import Option

class ReadOnlyLine(QLineEdit):
    'A read-only `QLineEdit`.'
    def __init__(self, contents: str):
        super().__init__(contents)
        self.setReadOnly(True)

class StringList(QTableView):
    '''Displays a list of strings with their index.

    We hijack a `QTableView` to display both the strings and their index.
    This means every string in the table is actually comprised of a row in a
    two-column table: one cell for ID, and one cell for string value.
    For the purposes of this class, "item" refers to the underlying string
    referenced by one of these rows.

    This widget has custom Slots and Signals so that an item can be selected
    by both its ID and string cell. Because of this, `selectionChanged` is not
    a very useful signal. Use `selectedItemChanged` instead.
    '''

    class Column(int):
        'Enum for differentiating table columns'
        ID = 0
        VALUE = 1

    class Model(QStandardItemModel):
        'A two-column model for holding strings and their IDs.'
        def __init__(self):
            super().__init__()
            self.setColumnCount(2)
            self.setHorizontalHeaderItem(0, QStandardItem('ID'))
            # TODO possibly allow overriding this label
            self.setHorizontalHeaderItem(1, QStandardItem('String'))

        def itemFromIndex(self, index: QModelIndex) -> 'StringList.Cell':
            return cast(StringList.Cell, super().itemFromIndex(index))

    class Cell(QStandardItem):
        'An cell in the list-table that cannot be directly edited.'
        def __init__(self, text: str):
            super().__init__(text)
            self.setEditable(False)

    class SelectionModel(QItemSelectionModel):
        'Gives us a new signal to fire when only the selected item in the table changes.'

        # Use Option to work around needing to define multiple connections.
        # This isn't that crazy. Qt's built-in handlers do this with QItemSelection.
        # See: https://stackoverflow.com/a/53108858 for what we're avoiding.
        selectedItemChanged = pyqtSignal(Option, Option)
        'Like `selectionChanged`, but only fires when the selected item changes.'

        def __init__(self, model: 'StringList.Model', parent: 'StringList'):
            super().__init__(model, parent)
            # Rationale: parent.selectedItemChanged is Callable, idk why mypy isn't seeing that.
            self.selectedItemChanged.connect(parent.selectedItemChanged) # type: ignore[arg-type]


    def __init__(self, items: List[str]):
        super().__init__()
        # TODO make ID column fit contents and be non-resizeable.
        # TODO make string column stretch to fit area.
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.verticalHeader().hide()

        model = StringList.Model()
        for index, string in enumerate(items):
            model.setItem(index, StringList.Column.ID,    StringList.Cell(str(index)))
            model.setItem(index, StringList.Column.VALUE, StringList.Cell(string))

        self.setModel(model)
        self.setSelectionModel(StringList.SelectionModel(model, self))

    def model(self) -> 'StringList.Model':
        'Functionally equivalent to `QTableView.model()`. Just changes return type.'
        return cast(StringList.Model, super().model())

    def selectionModel(self) -> 'StringList.SelectionModel':
        'Functionally equivalent to `QTableView.selectionModel()`. Just changes return type.'
        return cast('StringList.SelectionModel', super().selectionModel())

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        '''Slot called when selecting a cell in our list-table thing.

        Employs some hacky nonsense to make it so selecting an item's ID
        selects the item itself. Clients should use `selectedItemChanged` instead.
        '''
        super().selectionChanged(selected, deselected)

        selectedItem   = self._getSelectionItem(selected)
        deselectedItem = self._getSelectionItem(deselected)

        if selectedItem is None:
            return

        # Make selecting a value's ID count as selecting the value itself.
        # We always want to do this since it also controls the visual GUI.
        if selectedItem.column() == StringList.Column.ID:
            valueIndex = self.model().index(selectedItem.row(), StringList.Column.VALUE)
            self.selectionModel().select(valueIndex, QItemSelectionModel.SelectionFlag.ClearAndSelect)
            selectedItem = self.model().itemFromIndex(valueIndex)

        # Don't emit signal if we're toggling selection between a value and its ID.
        if  deselectedItem is not None \
        and selectedItem.row() == deselectedItem.row():
            return

        self.selectionModel().selectedItemChanged.emit(
            Option(selectedItem),
            Option(deselectedItem),
        )

    @pyqtSlot(Option, Option)
    def selectedItemChanged(
            self,
            selectedItem: 'Option[StringList.Cell]',
            deselectedItem: 'Option[StringList.Cell]',
    ) -> None:
        'Slot called when the selected item changes.'
        pass

    def _getSelectionItem(self, selection: QItemSelection) -> 'Optional[StringList.Cell]':
        '''Extracts the model referred to by the current selection.
        Assumes the given selection only contains a single model.
        '''
        if selection.isEmpty():
            return None

        indexes = selection.first().indexes()
        if len(indexes) == 0:
            return None

        # This is ok because we set SelectionMode.SingleSelection
        selectionIndex = indexes[0]
        return self.model().itemFromIndex(selectionIndex)
