from logging.handlers import RotatingFileHandler
import logging
import os
from .options import Options
from .config import *


def get_rotating_file_handler(options: Options, formatter: logging.Formatter) -> RotatingFileHandler:
    logs_dir_path = options.logs_dir_path or "logs"
    logs_dir_path = os.path.normpath(logs_dir_path)
    if not os.path.exists(logs_dir_path):
        os.makedirs(logs_dir_path)
    log_path = os.path.join(logs_dir_path, options.file_name)
    is_exists_log = os.path.exists(log_path)
    file_handler = RotatingFileHandler(log_path, maxBytes=options.max_MB * 1024 * 1024, backupCount=options.max_count,
                                       encoding="utf-8")
    if options.write_mode == "w" and is_exists_log:
        file_handler.doRollover()
    file_handler.setFormatter(formatter)
    return file_handler


def get_format_string(options: Options) -> str:
    format_string = options.format_string or default_format_string
    if format_string != default_format_string:
        return format_string
    if not options.show_name_label:
        format_string = format_string.replace(name_fs, "")
    if not options.show_location_label:
        format_string = format_string.replace(location_fs, "")
    return format_string
