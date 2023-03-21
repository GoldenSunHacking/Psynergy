from os.path import dirname
from pathlib import Path
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
        self.setWindowTitle('GS Neo Magic')
        self.setGeometry(50, 50, 600, 300)
        self.setAcceptDrops(True)

        # Sets up a main layout we can add and remove views (aka widgets) from.
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout()
        layout.addWidget(self.makeMenuBar())
        self.centralWidget().setLayout(layout)

        self.current_view = None
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
        if self.current_view:
            self.centralWidget().layout().removeWidget(self.current_view)

        self.current_view = viewWidget
        self.centralWidget().layout().addWidget(
            viewWidget, 100, Qt.AlignmentFlag.AlignTop
        )

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
            # TODO needs some kind of detection for invalid files from CLI
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
    # TODO disable tabs for editors we don't support for the loaded game
    bar = QTabWidget()
    bar.addTab(RomInfoTab(), 'ROM')
    bar.addTab(QLabel('TODO'), 'Map')
    bar.addTab(TextEditTab(), 'Text Editor')
    bar.addTab(QLabel('TODO'), 'Shops')
    bar.addTab(QLabel('TODO'), 'Abilities')
    bar.addTab(QLabel('TODO'), 'Party')
    bar.addTab(QLabel('TODO'), 'Elemental Data')
    bar.addTab(QLabel('TODO'), 'Encounters')
    bar.addTab(QLabel('TODO'), 'Forge')
    bar.addTab(QLabel('TODO'), 'Sprites')
    return bar
