import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = RotatingFileHandler(f'logs/{name}.log', maxBytes=20_000_000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
