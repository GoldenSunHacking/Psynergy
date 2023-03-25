from typing import List

from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow

# TODO we will probably want to create a state object we can read from for the UI.
# Saved config, themes, window locations, etc... go here

class PsynergyApp(QApplication):
    def __init__(self, argv: List[str]):
        super().__init__([])
        self._mainWindow = MainWindow()

        if len(argv) > 0:
            romFile = argv[0]
            self._mainWindow.openRomFile(romFile)

    def exec(self):
        self._mainWindow.show()

        # See event() below.
        self.startTimer(200)

        super().exec()

    # Allows exiting via interrupt (ctrl+c).
    #
    # By default, Python spends all of its time in native Qt land, meaning it
    # never gets a chance to handle our Python-level interrupt events.
    # This, combined with an app timer and a signal handler, occasionally makes
    # Qt give Python back control, so it can handle our interupts.
    #
    # See: https://stackoverflow.com/a/11705366/7954860
    def event(self, e):
        return super().event(e)
