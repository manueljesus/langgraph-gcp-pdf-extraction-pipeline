import os
import logging
from unittest.mock import patch, MagicMock
from src.logger import get_logger


class TestSetupLogger:
    @classmethod
    def setup_class(cls):
        """
        Clear the FUNCTION_NAME environment variable before running the tests.
        """
        if "FUNCTION_NAME" in os.environ:
            del os.environ["FUNCTION_NAME"]

    @classmethod
    def teardown_class(cls):
        """
        Clear the FUNCTION_NAME environment variable after running the tests.
        """
        if "FUNCTION_NAME" in os.environ:
            del os.environ["FUNCTION_NAME"]

    def test_get_logger_local_logging(self):
        """
        Test get_logger function when FUNCTION_NAME is not set (local logging).
        """
        with patch("src.logger.logging.FileHandler") as mock_file_handler, \
            patch("src.logger.logging.StreamHandler") as mock_stream_handler:

            # Mock the file and stream handlers
            mock_file_handler.return_value = MagicMock()
            mock_stream_handler.return_value = MagicMock()

            logger = get_logger("test_logger")

            # Check that the logger has a FileHandler
            mock_file_handler.assert_called_once_with("app.log")
            # Check that the logger has a StreamHandler
            mock_stream_handler.assert_called()
            # Ensure propagation is disabled
            assert logger.propagate is False

    def test_get_logger_google_cloud_logging(self):
        """
        Test get_logger function when FUNCTION_NAME is set (Google Cloud logging).
        """
        os.environ["FUNCTION_NAME"] = "test_function"
        with patch("src.logger.cloud_logging.Client") as mock_cloud_client, \
            patch("src.logger.logging.FileHandler") as mock_file_handler, \
            patch("src.logger.logging.StreamHandler") as mock_stream_handler:

            # Mock Google Cloud Logging Client
            mock_cloud_instance = MagicMock()
            mock_cloud_client.return_value = mock_cloud_instance

            # Mock the file and stream handlers (should not be called in cloud env)
            mock_file_handler.return_value = MagicMock()
            mock_stream_handler.return_value = MagicMock()

            logger = get_logger("test_logger")

            # Check that Google Cloud logging is configured
            mock_cloud_client.assert_called_once()
            mock_cloud_instance.setup_logging.assert_called_once_with(log_level=logging.INFO)

            # Check that no FileHandler or StreamHandler is added in cloud environment
            mock_file_handler.assert_not_called()
            mock_stream_handler.assert_not_called()

            # Ensure propagation is disabled
            assert logger.propagate is False
