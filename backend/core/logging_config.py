import logging
import os
from pathlib import Path

from backend.core.config import settings


def setup_logging() -> logging.Logger:
    log_dir = Path(settings.LOG_FILE).resolve().parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("inventory_platform")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(settings.LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


logger = setup_logging()
