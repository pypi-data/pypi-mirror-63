import logging
try:
    from zac import __version__ as version
except ImportError:
    version = 'UNKNOWN'


def create_logger(fname = None):
    logger = logging.getLogger(f'{__package__}-{version}')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    if fname is not None:
        fh = logging.FileHandler(fname)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)    
        logger.addHandler(fh)
    return logger
