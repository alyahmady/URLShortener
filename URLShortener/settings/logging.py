import os
from pathlib import Path

from .path import BASE_DIR
from .handler import env

LOGS_DIR = BASE_DIR / env.str("LOGS_DIR", "logs")

CORE_LOG_FILE = LOGS_DIR / env.str("CORE_LOG_FILENAME", "core.log")
ERROR_LOG_FILE = LOGS_DIR / env.str("ERROR_LOG_FILENAME", "error.log")
DEBUG_LOG_FILE = LOGS_DIR / env.str("DEBUG_LOG_FILENAME", "debug.log")

Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

for log_file in (
    CORE_LOG_FILE,
    ERROR_LOG_FILE,
    DEBUG_LOG_FILE,
):
    if not os.path.isfile(log_file):
        Path(log_file).touch()
