import logging


def get_logger():
    logging.basicConfig(
        format='%(asctime)s %(threadName)-12.12s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ])
    return logging.getLogger(__name__)


log = get_logger()
