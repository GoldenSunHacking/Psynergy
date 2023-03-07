from PyQt5 import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QMenuBar,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from .rom_info import makeRomInfoView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GS Neo Magic')
        self.setGeometry(50, 50, 320, 200)

        # TODO actually handle file drops
        self.setAcceptDrops(True)

        self.setCentralWidget(QWidget())
        # TODO need to know what we have opened here to select the view.
        self.applyView(makeDefaultView())

    def applyView(self, viewWidget):
        layout = QVBoxLayout()
        layout.addWidget(self.makeMenuBar(), 0)
        layout.addWidget(viewWidget, 100, Qt.AlignmentFlag.AlignTop)

        if self.centralWidget().layout():
            sip.delete(self.centralWidget().layout())
        self.centralWidget().setLayout(layout)

    def makeMenuBar(self):
        menuBar = QMenuBar()
        fileMenu = menuBar.addMenu('File')

        openAction   = fileMenu.addAction('Open...')
        saveAction   = fileMenu.addAction('Save')
        saveAsAction = fileMenu.addAction('Save As...')

        openAction.triggered.connect(lambda: self.applyView(makeEditorTabsView()))
        saveAction.triggered.connect(lambda: print('Clicked Save'))
        saveAsAction.triggered.connect(lambda: print('Clicked Save As'))

        return menuBar

def makeDefaultView():
    layout = QVBoxLayout()
    layout.addWidget(QLabel('No ROM opened. Open or drag+drop here.'))

    editorGroupBox = QGroupBox()
    editorGroupBox.setLayout(layout)

    return editorGroupBox

def makeEditorTabsView():
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
