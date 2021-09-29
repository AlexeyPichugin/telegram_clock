from telethon.client.telegramclient import TelegramClient


class TelegramClockError(Exception):
    """Base Telegram Clock error"""

    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}] {self.msg}"

    def __str__(self) -> str:
        return self.__repr__()


class ConfigError(TelegramClockError):
    """Config error"""

    pass


class ProxyConfigError(TelegramClockError):
    """Proxy config error"""

    pass


class LoggerConfigError(TelegramClient):
    """Logger config error"""

    pass


class SessionIsNotInit(TelegramClient):
    """Session is not init"""

    pass
