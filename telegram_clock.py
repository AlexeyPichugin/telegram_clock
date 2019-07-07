from telegram_clock.telegram_clock import Telegram_clock
from config import *
import argparse
import os

def _main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', help='Path to directory with numbers files', default=os.path.join(basedir,'data'), type=str)
    args = parser.parse_args()

    datadir = args.datadir

    print(API_ID, API_HASH)
    print(type(API_ID), type(API_HASH))

    with Telegram_clock(datadir, 'telegram_clock', API_ID, API_HASH) as conn:
        pass
        """
        while True:
            try:
                conn.run()
            except:
                break
        """

if __name__ == '__main__':
    print('Start project')
    _main()