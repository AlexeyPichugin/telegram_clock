from typing import Union, Optional, Dict, Any, Type

import os

from telegram_clock.exceptions import TelegramClockError

__all__ = ("get_config_from_dict_by_key", "get_env_variable")


def _get_value_by_name(
    dict: Union[Dict[str, Any], os._Environ],
    key: str,
    error_message: str,
    required: bool = True,
    default: Optional[Any] = None,
    ErrorCls: Type[TelegramClockError] = TelegramClockError,
) -> Any:
    """
    Get config value from dict and return it

    Args:
        config_dict (dict): dictionary with configs values
        key (str): key name
        required (bool): required flag (default True)
        default (Any): default value if key is not set
        ErrorCls (Type[TelegramClockError]): error TelegramClockError subclass
    Return:
        Value by key or default
    Raises:
        TelegramClockError if value is required
    """
    try:
        return dict[key]
    except KeyError:
        if required:
            raise ErrorCls(msg=error_message)
        else:
            return default


def get_config_from_dict_by_key(
    config_dict: Dict[str, Any],
    key: str,
    required: bool = True,
    default: Optional[Any] = None,
    ErrorCls: Type[TelegramClockError] = TelegramClockError,
) -> Any:
    """
    Get config value from configs dict and return it
    If not required and key is not found in config dict, return default value

    Args:
        config_dict (dict): dictionary with configs values
        key (str): key name
        required (bool): required flag (default True)
        default (Any): default value if key is not set
        ErrorCls (Type[TelegramClockError]): error TelegramClockError subclass
    Return:
        Value by key or default
    Raises:
        TelegramClockError if value is required
    """
    error_message = f'Key "{key}" is not set'
    return _get_value_by_name(
        config_dict, key, error_message=error_message, required=required, default=default, ErrorCls=ErrorCls
    )


def get_env_variable(
    var_name: str,
    required: bool = True,
    default: Optional[Any] = None,
    ErrorCls: Type[TelegramClockError] = TelegramClockError,
) -> Any:
    """
    Read environment variable and return it
    If variable is not required and not found, returns default value

    Args:
        var_name (str): variable name
        required (bool): required flag (default True)
        default (Any): default value if variable name is not found in env
        ErrorCls (Type[TelegramClockError]): error TelegramClockError subclass
    Returns:
        TelegramClockError if value is required and not found
    """
    error_message = f'Env variabe "{var_name}" is not set'
    return _get_value_by_name(
        os.environ, var_name, error_message=error_message, required=required, default=default, ErrorCls=ErrorCls
    )
