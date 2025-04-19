# from loguru import logger
# import sys
# import json
# from pathlib import Path
# from typing import Dict, Any
# from datetime import datetime
#
#
# def setup_logging(lvl: str = "DEBUG", rotation: str = "00:00"):
#     logger.remove()
#
#     console_fmt = (
#         "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
#         "<level>{level: <8}</level> |"
#         "<cyan>{module}</cyan>:<cyan>{function}</cyan> - "
#         "<level>{message}</level>"
#     )
#
#     def file_fmt(record: Dict[str, Any]) -> str:
#         log_record = {
#             "time": record["time"].isoformat(),
#             "level": record["level"].name,
#             "module": record["module"],
#             "function": record["function"],
#             "message": record["message"],
#             "extra": record["extra"],
#         }
#
#         # Handle exception info if present
#         if record["exception"] is not None:
#             log_record["exception"] = str(record["exception"])
#
#         return json.dumps(log_record)
#
#
#     logger.add(
#         sys.stderr,
#         level=lvl,
#         format=console_fmt,
#         colorize=True,
#         backtrace=True,
#         diagnose=True,
#     )
#
#     logs_dir = Path("logs")
#     logs_dir.mkdir(exist_ok=True)
#
#     logger.add(
#         logs_dir / "app_{time:YYYY-MM-DD}.log",
#         level="INFO",
#         format=file_fmt,
#         rotation=rotation,
#         compression="zip",
#         serialize=True,
#         enqueue=True,
#         catch=True
#     )
#
#     logger.add(
#         logs_dir / "errors.log",
#         level="ERROR",
#         format=file_fmt,
#         rotation="100 MB",
#         retention="30 days",
#         serialize=True,
#         backtrace=True,
#         diagnose=True
#     )
#
#     return logger

import os
import sys
import inspect
from datetime import datetime
from loguru import logger

LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

def set_logger_filename(filename: str):

    logger.remove()
    filename = filename if filename.endswith('.log') else filename + '.log'
    full_log_path = os.path.join(LOGS_DIR, filename)
    er_log_path = os.path.join(LOGS_DIR, 'error.log')


    console_fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
        "<level>{level: <8}</level> |"
        "<cyan>{module}</cyan>:<cyan>{function}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stderr,
        level='DEBUG',
        format=console_fmt,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        full_log_path,
        level='DEBUG',
        rotation='00:00',
        colorize=False,
        backtrace=True,
        diagnose=True,
        enqueue=True,
        encoding='utf-8'
    )
    logger.add(
        er_log_path,
        level='ERROR',
        rotation='00:00',
        enqueue=True,
        encoding='utf-8',
        colorize=False,
        backtrace=True,
        diagnose=True,
    )

    return logger

def set_logger_auto():

    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__ if module else 'unknown'

    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'bot_{module_name}_{date_str}.log'
    return set_logger_filename(filename)

