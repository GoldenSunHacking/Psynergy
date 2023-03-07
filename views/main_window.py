from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QMenuBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from .rom_info import makeRomInfoView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # TODO actually handle file drops
        self.setAcceptDrops(True)
        # TODO need to know what we have opened here to select the view.
        self.applyView(makeDefaultView())

    def applyView(self, viewWidget):
        outerLayout = QVBoxLayout()
        outerLayout.addWidget(makeMenuBar(), 0)
        outerLayout.addWidget(viewWidget, 100, Qt.AlignmentFlag.AlignTop)

        self.setLayout(outerLayout)

def makeMenuBar():
    menuBar = QMenuBar()
    actionFile = menuBar.addMenu('File')
    actionFile.addAction('Open...')
    actionFile.addAction('Save')
    actionFile.addAction('Save As...')
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
