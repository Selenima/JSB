from loguru import logger
import sys
import json
from pathlib import Path

def setup_logging(lvl: str = "DEBUG", rotation: str = "10 MB"):

    logger.remove()

    console_fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
        "<level>{level: <8}</level> |"
        "<cyan>{module}</cyan>:<cyan>{function}</cyan> - "
        "<level>{message}</level>"
    )

    file_fmt = lambda record: json.dumps({
        "time": record["time"].isoformat(),
        "level": record["level"].name,
        "module": record["module"],
        "function": record["function"],
        "message": record["message"],
        "extra": record["extra"],
    })

    logger.add(
        sys.stderr,
        level=lvl,
        format=console_fmt,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger.add(
        logs_dir / "bot_{time}.log",
        level="INFO",
        format=file_fmt,
        rotation=rotation,
        compression="zip",
        serialize=True
    )

    logger.add(
        logs_dir / "errors.log",
        level="ERROR",
        format=file_fmt,
        rotation="100 MB",
        retention="30 days",
    )

    return logger
