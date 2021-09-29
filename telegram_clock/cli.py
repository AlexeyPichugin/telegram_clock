from pathlib import Path
from telegram_clock.telegram_clock import TelegramClockClient

from dotenv import load_dotenv

import argparse
import os


def init_args() -> argparse.Namespace:
    """Read CLI arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./configs/config.yaml", help="Path to config file")
    parser.add_argument("--api-id", type=str, default=None, help="Telegram API_ID")
    parser.add_argument("--api-hash", type=str, default=None, help="Telegram API_HASH")
    parser.add_argument("--session", type=str, default=None, help="Session string")
    parser.add_argument("--phone-number", type=str, default=None, help="Telegram client phone number")
    parser.add_argument("--password", type=str, default=None, help="Telegram 2 factor password")
    parser.add_argument("--init", action="store_true", help="Run init script")
    return parser.parse_args()


def run() -> None:
    """Run application"""
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    args = init_args()
    if args.api_id is not None:
        os.environ["API_ID"] = args.api_id
    if args.api_hash is not None:
        os.environ["API_HASH"] = args.api_hash
    if args.phone_number is not None:
        os.environ["TELEGRAM_PHONE"] = args.phone_number
    if args.password is not None:
        os.environ["TELEGRAM_PASSWORD"] = args.password
    if args.session is not None:
        os.environ["TELEGRAM_SESSION"] = args.password

    config_path = args.config if os.path.isabs(args.config) else os.path.abspath(args.config)
    telegram_clock_client = TelegramClockClient(config_path=config_path)
    try:
        telegram_clock_client.run_application() if not args.init else telegram_clock_client.print_session_string()
    finally:
        telegram_clock_client.close()
