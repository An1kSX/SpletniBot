__all__ = ["ModuleLogger"]

import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


class ModuleLogger:
    def __init__(
        self,
        module_name: str,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
        to_console: bool = True,
        to_file: bool = False,
    ):
        self.logger = self._create_logger(
            module_name=module_name,
            max_bytes=max_bytes,
            backup_count=backup_count,
            to_console=to_console,
            to_file=to_file,
        )

    @staticmethod
    def _create_logger(
        module_name: str,
        max_bytes: int,
        backup_count: int,
        to_console: bool,
        to_file: bool,
    ) -> logging.Logger:
        logger = logging.getLogger(module_name)

        level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(level)

        # Если уже настроен — не трогаем handlers (важно при множественных импортах)
        if logger.handlers:
            return logger

        logger.propagate = False

        formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]\n\t\t\t%(message)s")

        if to_console:
            console_handler = StreamHandler(stream=sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if to_file:
            log_dir = "./logs"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{module_name}.log")

            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger
