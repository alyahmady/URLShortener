import logging
from pathlib import Path

from django.conf import settings


def setup_logger(name: str, log_file: Path | str, level: int = logging.DEBUG):
    formatter = logging.Formatter(
        fmt="%(levelname)s: %(asctime)s | %(funcName)s => %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.FileHandler(log_file, mode="a")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


core_logger = setup_logger(
    name="URLShortenerCore", log_file=settings.CORE_LOG_FILE, level=logging.DEBUG
)
core_logger.info("Starting core logger")

error_logger = setup_logger(
    name="Errors", log_file=settings.ERROR_LOG_FILE, level=logging.DEBUG
)
error_logger.info("Starting error logger")

debug_logger = setup_logger(
    name="DebugErrors", log_file=settings.DEBUG_LOG_FILE, level=logging.DEBUG
)
debug_logger.info("Starting debug logger")
