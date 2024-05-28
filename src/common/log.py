"""Module."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from loguru import logger

from src.config.base import settings
from src.config.path_conf import LOG_DIR

if TYPE_CHECKING:
    import loguru


class Logger:
    """_summary_."""

    def __init__(self):
        """_summary_."""
        self.log_path = LOG_DIR

    def log(self) -> loguru.Logger:
        """_summary_.

        Returns:
            loguru.Logger: _description_
        """
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        log_stdout_file = os.path.join(
            self.log_path, settings.LOG_STDOUT_FILENAME
        )
        log_stderr_file = os.path.join(
            self.log_path, settings.LOG_STDERR_FILENAME
        )

        log_config = {
            "rotation": "10 MB",
            "retention": "15 days",
            "compression": "tar.gz",
            "enqueue": True,
        }
        # stdout
        logger.add(
            log_stdout_file,
            level="INFO",
            filter=lambda record: record["level"].name == "INFO"
            or record["level"].no <= 25,
            **log_config,
            backtrace=False,
            diagnose=False,
        )
        # stderr
        logger.add(
            log_stderr_file,
            level="ERROR",
            filter=lambda record: record["level"].name == "ERROR"
            or record["level"].no >= 30,
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        return logger


log = Logger().log()
