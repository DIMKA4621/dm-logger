from logging.handlers import RotatingFileHandler
from typing import Callable, Literal
import logging
import os.path
import sys
import re


class DMLogger:
    def __init__(
        self,
        name: str,
        logging_level: str = "DEBUG",
        logs_dir_path: str = "logs",
        print_logs: bool = True,
        file_name: str = "",
        write_mode: Literal["a", "w"] = "w",
        max_MB: int = 5,
        max_count: int = 10,
        format_string: str = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(module)s.%(funcName)s:%(lineno)d) %(message)s",
    ):
        self._logger = logging.getLogger(name)
        level = logging.getLevelName(logging_level.upper())
        self._logger.setLevel(level)
        formatter = logging.Formatter(format_string, datefmt='%d-%m-%Y %H:%M:%S')

        if logs_dir_path:
            logs_dir_path = os.path.normpath(logs_dir_path)
            if not os.path.exists(logs_dir_path):
                os.makedirs(logs_dir_path)
            file_name = file_name or f"{name}.log"
            log_path = os.path.join(logs_dir_path, file_name)
            is_exists_log = os.path.exists(log_path)

            file_handler = RotatingFileHandler(log_path, maxBytes=max_MB * 1024 * 1024, backupCount=max_count)
            if write_mode == "w" and is_exists_log:
                file_handler.doRollover()
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        if print_logs:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_handler.addFilter(DebugInfoFilter())
            stdout_handler.setFormatter(formatter)

            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.WARNING)
            stderr_handler.addFilter(WarningErrorCriticalFilter())
            stderr_handler.setFormatter(formatter)

            self._logger.addHandler(stdout_handler)
            self._logger.addHandler(stderr_handler)

    def debug(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.debug, message, **kwargs)

    def info(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.info, message, **kwargs)

    def warning(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.warning, message, **kwargs)

    def error(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.error, message, **kwargs)

    def critical(self, message: any = None, **kwargs) -> None:
        self._log(self._logger.critical, message, **kwargs)

    @staticmethod
    def _log(level_func: Callable, message: any, **kwargs) -> None:
        message = "- " + str(message) if not (message is None) else ""
        if kwargs:
            dict_string = re.sub(r"'(\w+)':", r"\1:", str(kwargs))
            message = f"{dict_string} {message}"
        level_func(message)

class DebugInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.DEBUG, logging.INFO)

class WarningErrorCriticalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL)