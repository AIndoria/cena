import logging
import sys

from cena.core.config import DATA_DIR

LOGGER_FILE = DATA_DIR.joinpath("cena.log")
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOGGER_FORMAT = "%(levelname)s: %(asctime)s \t%(message)s"

logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT, datefmt="%d-%b-%y %H:%M:%S")


def logger_init() -> logging.Logger:
    """ Returns the Root Loggin Object for Cena """
    logger = logging.getLogger("cena")
    logger.propagate = False

    # File Handler
    output_file_handler = logging.FileHandler(LOGGER_FILE)
    handler_format = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)
    output_file_handler.setFormatter(handler_format)

    # Stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(handler_format)

    logger.addHandler(output_file_handler)
    logger.addHandler(stdout_handler)

    return logger


root_logger = logger_init()


def get_logger(module=None) -> logging.Logger:
    """ Returns a child logger for cena """
    global root_logger

    if module is None:
        return root_logger

    return root_logger.getChild(module)
