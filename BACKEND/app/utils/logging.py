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
        "<green>{time:YYYY-MM-DD}</green> |"
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
    filename = f'app_{module_name}_{date_str}.log'
    return set_logger_filename(filename)

