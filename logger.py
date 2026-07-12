"""
Vyache Failover
Logger

Author: HaiKu
Version: 1.0.0
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


class Logger:

    def __init__(self, logfile: str):

        Path(logfile).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logger = logging.getLogger(
            "vyache-failover"
        )

        # Чтоб при повторном импорте обработсики не плодились :З
        if self.logger.handlers:
            return

        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(
            logfile,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(
            sys.stdout
        )

        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):

        self.logger.info(message)

    def warning(self, message: str):

        self.logger.warning(message)

    def error(self, message: str):

        self.logger.error(message)

    def critical(self, message: str):

        self.logger.critical(message)

    def exception(self, message: str):

        self.logger.exception(message)
