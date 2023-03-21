from argparse import ArgumentParser
from pathlib import Path
from signal import signal, SIGINT
from sys import exit

from app import PsynergyApp

arg_parser = ArgumentParser(
    description='Graphical editor for Golden Sun and other Camelot games.',
    prog='psynergy',
)
arg_parser.add_argument('-v', '--version', action='version', version='0.0.0-dev')
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
