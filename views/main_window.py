from os.path import dirname
from pathlib import Path
from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDropEvent
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QLabel,
    QMenuBar,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from data.rom_loader import Rom

from .rom_info import makeRomInfoView
from .state import state

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GS Neo Magic')
        self.setGeometry(50, 50, 320, 200)
        self.setAcceptDrops(True)

        self.setCentralWidget(QWidget())
        # TODO need to know what we have opened here to select the view.
        self.applyView(makeDefaultView())

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        '''Event handler for hovering over the window with a dragged file.
        Only allows subsequent `dropEvent` to fire if the file is a ROM file.
        '''
        if e.mimeData().hasUrls() \
        and Path(e.mimeData().urls()[0].fileName()).suffix in ['.gba', '.nds']:
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent) -> None:
        'Event handler for dropping a dragged ROM file into the window.'
        self.openRomFile(e.mimeData().urls()[0].toLocalFile())

    def applyView(self, viewWidget: QWidget) -> None:
        'Replaces the content of the main window with the given Widget.'
        layout = QVBoxLayout()
        layout.addWidget(self.makeMenuBar(), 0)
        layout.addWidget(viewWidget, 100, Qt.AlignmentFlag.AlignTop)

        if self.centralWidget().layout():
            sip.delete(self.centralWidget().layout())
        self.centralWidget().setLayout(layout)

    def makeMenuBar(self) -> QMenuBar:
        'Creates the menu bar widget for the top of the main window.'
        menuBar = QMenuBar()
        fileMenu = menuBar.addMenu('File')

        openAction   = fileMenu.addAction('Open...')
        saveAction   = fileMenu.addAction('Save')
        saveAsAction = fileMenu.addAction('Save As...')

        openAction.triggered.connect(self.openRomFileDialog)
        saveAction.triggered.connect(lambda: print('Clicked Save'))
        saveAsAction.triggered.connect(lambda: print('Clicked Save As'))

        return menuBar

    def openRomFileDialog(self) -> None:
        'Opens a ROM file using a file selection dialog.'
        filename = QFileDialog().getOpenFileName(
            caption='Open a GBA/NDS File',
            filter='GBA/NDS file (*.gba *.nds)',
            directory=state.working_dir,
        )[0]
        # Save this so subsequent file dialogs can open straight to this dir.
        state.working_dir = dirname(filename)
        self.openRomFile(filename)

    def openRomFile(self, filepath: str) -> None:
        'Opens a ROM file from a file path.'
        try:
            state.loaded_rom = Rom(filepath)
            self.applyView(makeEditorTabsView())
        except Exception as e:
            # TODO better error handling. Probably print to window
            print(e)

def makeDefaultView() -> QGroupBox:
    layout = QVBoxLayout()
    layout.addWidget(QLabel('No ROM opened. Open or drag+drop here.'))

    editorGroupBox = QGroupBox()
    editorGroupBox.setLayout(layout)

    return editorGroupBox

def makeEditorTabsView() -> QTabWidget:
    bar = QTabWidget()
    bar.addTab(makeRomInfoView(), 'ROM')
    bar.addTab(QLabel('TODO'), 'Map')
    bar.addTab(QLabel('TODO'), 'Text Editor')
    bar.addTab(QLabel('TODO'), 'Shops')
    bar.addTab(QLabel('TODO'), 'Abilities')
    bar.addTab(QLabel('TODO'), 'Party')
    bar.addTab(QLabel('TODO'), 'Elemental Data')
    bar.addTab(QLabel('TODO'), 'Encounters')
    bar.addTab(QLabel('TODO'), 'Forge')
    bar.addTab(QLabel('TODO'), 'Sprites')
    return bar
