"""Set logging """

import logging


def logging_setup(log_path: str, log_prefix:str, console_only: bool=False) -> None:
    logger = logging.getLogger(log_prefix)
    logger.setLevel(logging.DEBUG)
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(log_path, mode='w')
    if not console_only:
        file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if not console_only:
        logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Logging setup completed.\n")
    return logger
