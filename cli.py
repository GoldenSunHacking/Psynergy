from signal import signal, SIGINT
from sys import exit

from app import MagicApp

# This is where things like CLI argument handling goes

# TODO argv handling?
app = MagicApp([])

def handleInterrupt(sig, frame):
    print('Unclean exit via interrupt!')
    app.quit()
    exit()

if __name__ == '__main__':
    signal(SIGINT, handleInterrupt)
    exit(app.exec())
