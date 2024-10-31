from logging import getLogger, basicConfig, StreamHandler, FileHandler, Formatter, Logger, DEBUG
from typing import Optional


def initialise_logger(
        file_path: Optional[str] = "test_log.log",
        level: int = DEBUG,
        message_format: str = "[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)s] %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> Logger:
    logger: Logger = getLogger(__name__)
    
    basicConfig(
        format = message_format,
        datefmt = date_format,
        level = level,
        handlers=[StreamHandler()]
    )

    if file_path is not None:
        file_handler = FileHandler(filename = file_path)
        file_handler.setLevel(level = level)
        file_handler.setFormatter(Formatter(message_format, date_format))
        logger.addHandler(file_handler)

        logger.debug(f"Logging to file path: {file_path}")
    
    logger.debug(f"Logging configured using level: {level}")

    return logger
