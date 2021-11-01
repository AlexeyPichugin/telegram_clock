from typing import Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger, _Logger  # type: ignore

import yaml
import sys
import os

from telegram_clock.exceptions import ConfigError, ProxyConfigError, LoggerConfigError
from telegram_clock.utils import get_config_from_dict_by_key, get_env_variable


@dataclass
class ProxyConfig:
    """Proxy config object"""

    type: str
    host: str
    port: int
    secret: Optional[str] = None

    @classmethod
    def from_dict(cls, proxy_dict: Dict[str, Any]) -> "ProxyConfig":
        """Get config from dict"""
        type: str = get_config_from_dict_by_key(proxy_dict, "type", ErrorCls=ProxyConfigError)
        if type.upper() not in ("MTPROTO", "SOCKS5"):
            raise ProxyConfigError('Proxy type must be one of {"MTProto", "SOCKS5"}')
        host: str = get_config_from_dict_by_key(proxy_dict, "host", ErrorCls=ProxyConfigError)
        port: int = get_config_from_dict_by_key(proxy_dict, "port", ErrorCls=ProxyConfigError)
        secret: str = get_config_from_dict_by_key(proxy_dict, "secret", required=False, ErrorCls=ProxyConfigError)
        if secret is None and type.upper() == "MTPROTO":
            raise ProxyConfigError('Not set "secret" for MTProto proxy')
        return cls(type=type, host=host, port=port, secret=secret)


@dataclass
class LoggerConfig:
    log_level: str = "INFO"
    log_to_file: bool = False
    log_file_name: str = "telegram.log"
    log_file_max_size: int = 8

    def get_logger(self) -> _Logger:
        logger.remove()

        logger_format = "{time} [{level}] {module}:{function}:{line} {message}"
        logger.add(sys.stdout, level=self.log_level, format=logger_format)
        if self.log_to_file:
            os.makedirs(os.path.dirname(self.log_file_name), exist_ok=True)
            logger.add(
                self.log_file_name, level=self.log_level, format=logger_format, rotation=f"{self.log_file_max_size} MB"
            )
        return logger.opt()

    @classmethod
    def from_dict(cls, logger_dict: Dict[str, Any]) -> "LoggerConfig":
        log_level = get_config_from_dict_by_key(
            logger_dict,
            "log_level",
            required=False,
            default="INFO",
            ErrorCls=LoggerConfigError,
        ).upper()
        if log_level not in ("DEBUG", "INFO", "WARNING", "ERROR"):
            raise LoggerConfigError('Log level must be one of {"DEBUG", "INFO", "WARNING", "ERROR}"}')

        log_to_file = get_config_from_dict_by_key(
            logger_dict,
            "log_to_file",
            required=False,
            default=False,
            ErrorCls=LoggerConfigError,
        )
        log_file_name = get_config_from_dict_by_key(
            logger_dict,
            "log_file_name",
            required=False,
            default="telegram_clock.log",
            ErrorCls=LoggerConfigError,
        )
        log_file_max_size = get_config_from_dict_by_key(
            logger_dict,
            "log_file_max_size",
            required=False,
            default=8,
            ErrorCls=LoggerConfigError,
        )
        return cls(
            log_level=log_level,
            log_to_file=log_to_file,
            log_file_name=log_file_name,
            log_file_max_size=log_file_max_size,
        )


@dataclass
class Config:
    """
    Config object
    Attributes:
        api_id (str): API ID
        api_hash (str): API HASH
        phone_number (str): telegram account phone number
        password (str): telegram account 2-factor password (if set)
        session (str): session string
        data_dir (str): directory with files with images
        session_name (str): application session name
        use_ipv6 (bool): ipv6 flag
        timeout (int): timeout in secconds
        proxy (ProxyConfig): proxy config or None
        logger (LoggerConfig): logger config
    """

    api_id: int
    api_hash: str
    phone_number: Optional[str] = None
    password: Optional[str] = None
    session: Optional[str] = None
    data_dir: str = "./data"
    use_ipv6: bool = False
    timeout: int = 10
    proxy: Optional[ProxyConfig] = None
    logger: LoggerConfig = LoggerConfig()

    @classmethod
    def from_yaml(cls, path_to_config: str) -> "Config":
        """
        Read config from yaml file

        Args:
            path_to_config: path to yaml config file
        Returns:
            Config object
        Raises:
            ProxyConfigError if error occurred while reading
        """
        api_id = get_env_variable("API_ID", ErrorCls=ConfigError)
        if not api_id.isdigit():
            raise ConfigError("API_ID must be integer")
        api_hash = get_env_variable("API_HASH", ErrorCls=ConfigError)
        phone_number = get_env_variable("TELEGRAM_PHONE", ErrorCls=ConfigError, required=False)
        password = get_env_variable("TELEGRAM_PASSWORD", ErrorCls=ConfigError, required=False)
        if not os.path.exists(path_to_config):
            raise ConfigError("Config file is not found")
        session = get_env_variable("TELEGRAM_SESSION", ErrorCls=ConfigError, required=False)

        with open(path_to_config) as config_fd:
            config_dict = yaml.load(config_fd, Loader=yaml.SafeLoader)
        data_dir = get_config_from_dict_by_key(config_dict, "data_dir", ErrorCls=ConfigError)
        use_ipv6 = get_config_from_dict_by_key(config_dict, "use_ipv6", required=False, default=False)

        timeout = get_config_from_dict_by_key(config_dict, "timeout", required=False, default=10)
        proxy_dict = get_config_from_dict_by_key(config_dict, "proxy", required=False, ErrorCls=ConfigError)
        proxy = ProxyConfig.from_dict(proxy_dict) if proxy_dict is not None else None
        logger_dict = get_config_from_dict_by_key(config_dict, "logger", required=False, ErrorCls=ConfigError)
        logger = LoggerConfig() if logger_dict is None else LoggerConfig.from_dict(logger_dict)

        return cls(
            api_id=int(api_id),
            api_hash=api_hash,
            phone_number=phone_number,
            password=password,
            session=session,
            use_ipv6=use_ipv6,
            timeout=timeout,
            data_dir=data_dir,
            proxy=proxy,
            logger=logger,
        )
