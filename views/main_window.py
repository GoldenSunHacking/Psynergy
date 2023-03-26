from os.path import dirname
from pathlib import Path
from typing import cast

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
from info import PROGRAM_NAME

from .rom_info import RomInfoTab
from .state import state
from .text_editor import TextEditTab

class MainWindow(QMainWindow):
    '''The top-level window.
    Contains the top menu bar and the editor tabs.
    Can open ROM files via the menu or drag+drop.
    '''

    def __init__(self):
        super().__init__()
        # TODO make contents stretch to fit window size
        self.setWindowTitle(PROGRAM_NAME)
        self.setGeometry(50, 50, 600, 300)
        self.setAcceptDrops(True)

        # Sets up a main layout we can add and remove views (aka widgets) from.
        self.setCentralWidget(QWidget(self))
        layout = QVBoxLayout()
        layout.addWidget(self._makeMenuBar())
        self.centralWidget().setLayout(layout)

        self._currentView = None
        self.applyView(self._makeDefaultView())

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
        if self._currentView:
            self.centralWidget().layout().removeWidget(self._currentView)

        self._currentView = viewWidget
        cast(QVBoxLayout, self.centralWidget().layout()).addWidget(
            viewWidget, 100, Qt.AlignmentFlag.AlignTop
        )

    def _makeMenuBar(self) -> QMenuBar:
        'Creates the menu bar widget for the top of the main window.'
        menuBar = QMenuBar(self)
        fileMenu = menuBar.addMenu('File')

        openAction   = fileMenu.addAction('Open...')
        saveAction   = fileMenu.addAction('Save')
        saveAsAction = fileMenu.addAction('Save As...')

        openAction.triggered.connect(self.openRomFileDialog)
        # TODO wire these up to something
        saveAction.triggered.connect(lambda: print('Clicked Save'))
        saveAsAction.triggered.connect(lambda: print('Clicked Save As'))

        return menuBar

    def openRomFileDialog(self) -> None:
        'Opens a ROM file using a file selection dialog.'
        filename = QFileDialog().getOpenFileName(
            caption='Open a GBA/NDS File',
            filter='GBA/NDS file (*.gba *.nds)',
            # Rationale: this parameter properly handles None
            directory=state.workingDir, # type: ignore[arg-type]
        )[0]
        # Save this so subsequent file dialogs can open straight to this dir.
        state.workingDir = dirname(filename)
        self.openRomFile(filename)

    def openRomFile(self, filepath: str) -> None:
        'Opens a ROM file from a file path.'
        try:
            # TODO needs some kind of detection for invalid files from CLI
            state.loadedRom = Rom(filepath)
            self.applyView(self._makeEditorTabsView())
        except Exception as e:
            # TODO better error handling. Probably print to window
            print(e)

    def _makeDefaultView(self) -> QGroupBox:
        layout = QVBoxLayout()
        layout.addWidget(QLabel('No ROM opened. Open or drag+drop here.'))

        editorGroupBox = QGroupBox(self)
        editorGroupBox.setLayout(layout)

        return editorGroupBox

    def _makeEditorTabsView(self) -> QTabWidget:
        # TODO disable tabs for editors we don't support for the loaded game
        bar = QTabWidget(self)
        bar.addTab(RomInfoTab(bar), 'ROM')
        bar.addTab(QLabel('TODO'), 'Map')
        bar.addTab(TextEditTab(bar), 'Text Editor')
        bar.addTab(QLabel('TODO'), 'Shops')
        bar.addTab(QLabel('TODO'), 'Abilities')
        bar.addTab(QLabel('TODO'), 'Party')
        bar.addTab(QLabel('TODO'), 'Elemental Data')
        bar.addTab(QLabel('TODO'), 'Encounters')
        bar.addTab(QLabel('TODO'), 'Forge')
        bar.addTab(QLabel('TODO'), 'Sprites')
        return bar
