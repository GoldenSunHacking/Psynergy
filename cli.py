from argparse import ArgumentParser
from pathlib import Path
from signal import signal, SIGINT
from sys import exit

from app import PsynergyApp
from info import PROGRAM_DESCRIPTION, PROGRAM_NAME, PROGRAM_VERSION

arg_parser = ArgumentParser(
    description=PROGRAM_DESCRIPTION,
    prog=PROGRAM_NAME.lower(),
)
arg_parser.add_argument('-v', '--version', action='version', version=PROGRAM_VERSION)
arg_parser.add_argument('file', type=Path, nargs='?', help='ROM file to open.')

if __name__ == '__main__':
    args = arg_parser.parse_args()

    app = PsynergyApp([str(args.file)] if args.file else [])

    def handleInterrupt(sig, frame):
        print('Unclean exit via interrupt!')
        app.quit()
        exit()
    signal(SIGINT, handleInterrupt)

    exit(app.exec())
