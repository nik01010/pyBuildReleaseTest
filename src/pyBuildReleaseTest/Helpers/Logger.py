from logging import getLogger, basicConfig, getLevelName, StreamHandler, FileHandler, Handler, Logger, DEBUG
from typing import Optional, List


def initialise_logger(
        file_path: Optional[str] = "test_log.log",
        level: int = DEBUG,
        message_format: str = "[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)s] %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> Logger:
    logger: Logger = getLogger(__name__)
    
    if file_path is None:
        handlers: List[Handler] = [StreamHandler()]
    else:
        handlers: List[Handler] = [
            FileHandler(filename = file_path),
            StreamHandler()
        ]

    basicConfig(
        format = message_format,
        datefmt = date_format,
        level = level,
        handlers = handlers
    )

    level_name: str = getLevelName(level)
    logger.debug(f"Logging configured using level: {level_name}")

    if file_path is not None:
        logger.debug(f"Logging to file path: {file_path}")

    return logger
