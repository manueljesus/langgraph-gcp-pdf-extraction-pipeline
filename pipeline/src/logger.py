import logging
import os
from google.cloud import logging as cloud_logging

def get_logger(name):
    """
    Sets up a logger with the specified name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Clear existing handlers to prevent duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    # Disable propagation to avoid duplicate logs
    logger.propagate = False

    google_cloud_logging = os.getenv("FUNCTION_NAME") is not None

    if google_cloud_logging:
        # Use Google Cloud Logging in production
        client = cloud_logging.Client()
        client.setup_logging(log_level=logging.INFO)
        # Do not add additional handlers in cloud environment
    else:
        # Local development logging: File + Console
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # FileHandler for local development
        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

        # Console handler for local development
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)

    return logger
