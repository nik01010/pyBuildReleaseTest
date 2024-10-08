import logging

def initialise_logger(
        log_file_path: str = "test_log.log",
        log_level: int = logging.DEBUG,
        log_message_format: str = "[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)s] %(message)s",
        log_date_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(__name__)

    logging.basicConfig(
        format = log_message_format,
        datefmt = log_date_format,
        level = log_level,
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

    return logger
