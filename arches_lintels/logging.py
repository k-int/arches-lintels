import logging

def configure_logging():

    logger = logging.getLogger('lintels')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('lintels.log')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
