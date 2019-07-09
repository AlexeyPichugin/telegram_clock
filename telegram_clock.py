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
    parser.add_argument('-p', '--proxy', help='Use proxy? (default: True)', action="store_false")
    parser.add_argument('--proxy_mode', help='If use proxy, choise the connection mode (default: MTProto)', choices=['MTProto', 'SOCKS5'], default='MTProto')
    parser.add_argument('--proxy_server', 
        help='Input proxy setver by format "host, port, secret". If proxy_mode is SOCKS5, secret must be empty. If MTProto has not secret, input "None"', 
        default="russia-dd.proxy.digitalresistance.dog, 443, ddd41d8cd98f00b204e9800998ecf8427e", 
        type=str
    )
    args = parser.parse_args()

    if os.environ.get('API_ID') is None:
        API_ID = input('Input your API_ID: ')

    if os.environ.get('API_HASH') is None:
        API_HASH = input('Input your API_HASH: ')

    

    datadir = args.datadir
    proxy_flg = args.proxy
    proxy_mode = args.proxy_mode
    proxy_server = args.proxy_server

    try:
        proxy_host = str(proxy_server.split(',')[0].strip())
        proxy_port= int(proxy_server.split(',')[1].strip())
        proxy_secret = str(proxy_server.split(',')[2].strip())
    except:
        print('Incorrect proxy server srting')
        exit()
    
    conn = None
    proxy = None
    if proxy_flg:
        if proxy_mode == 'MTProto':
            from telethon import connection
            conn = connection.ConnectionTcpMTProxyRandomizedIntermediate
            proxy=(proxy_host, proxy_port, proxy_secret)
        elif proxy_mode == 'SOCKS5':
            import socks
            proxy = (socks.SOCKS5, proxy_host, proxy_port)

    try:
        with Telegram_clock(datadir=datadir, con_name='telegram clock', api_id=API_ID, api_hash=API_HASH, proxy=proxy, connection=conn) as conn:
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