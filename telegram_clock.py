from telegram_clock.telegram_clock import Telegram_clock
from config import API_ID, API_HASH
import argparse
import os
import socks
import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/logfile.log', maxBytes=10*1024*1024, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)

logger = logging.getLogger('telegram_clock')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def _main(API_ID, API_HASH):
    basedir = os.path.abspath(os.path.dirname(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', help='Path to directory with numbers files', default=os.path.join(basedir,'data'), type=str)
    args = parser.parse_args()

    if os.environ.get('API_ID') is None:
        API_ID = input('Input your API_ID: ')

    if os.environ.get('API_HASH') is None:
        API_HASH = input('Input your API_HASH: ')

    datadir = args.datadir
    try:
        with Telegram_clock(datadir=datadir, con_name='telegram clock', api_id=API_ID, api_hash=API_HASH, proxy=(socks.SOCKS5, '75.119.200.128', 2719)) as conn:
            while True:
                try:
                    conn.run()
                except:
                    logger.error('Error update photo')
    except:
        logger.error('Error connect to telegram')
           

if __name__ == '__main__':
    logger.info('Start project')
    _main(API_ID, API_HASH)