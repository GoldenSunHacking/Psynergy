from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow

# TODO we will probably want to create a state object we can read from for the UI.
# Saved config, themes, window locations, etc... go here
def startApp():
    app = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    return app.exec()
