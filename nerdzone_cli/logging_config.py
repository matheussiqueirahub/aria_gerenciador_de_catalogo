from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger() -> logging.Logger:
    return logging.getLogger("nerdzone")


def configure_logging(log_file: str | None = None) -> None:
    logger = get_logger()
    if logger.handlers:
        return
    logger.setLevel(logging.INFO)

    path = log_file or os.path.join("logs", "estoque.log")
    pasta = os.path.dirname(os.path.abspath(path))
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)

    handler = RotatingFileHandler(path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

