import logging
import os
from google.cloud import logging as cloud_logging


def get_logger(name):
    """
    Sets up a logger with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    google_cloud_logging = os.getenv("FUNCTION_NAME") is not None

    if google_cloud_logging:
        client = cloud_logging.Client()
        client.setup_logging(log_level=logging.INFO)
    else:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    # Console handler for both environments
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    return logger
