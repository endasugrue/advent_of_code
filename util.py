import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('advent_of_code')

def setup_logging(logger, console_level=logging.INFO, file_level=logging.DEBUG):
    logger = logging.getLogger(logger)
    logger.setLevel(logging.DEBUG)
    
    c_handle = logging.StreamHandler()
    c_handle.setLevel(console_level)

    f_handle = RotatingFileHandler('advent_of_code.log', maxBytes=2000000, backupCount=5)
    f_handle.setLevel(file_level)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')

    c_handle.setFormatter(formatter)
    f_handle.setFormatter(formatter)

    logger.addHandler(c_handle)
    logger.addHandler(f_handle)