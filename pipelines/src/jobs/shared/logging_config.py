
import logging

def setup_logger():
    logger = logging.getLogger('numbersff-pipelines')
    logger.setLevel(logging.INFO)


    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    return logger

# Create and configure the logger
logger = setup_logger()