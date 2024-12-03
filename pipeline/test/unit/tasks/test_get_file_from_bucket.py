import io
import pytest
from typing import Generator
from unittest.mock import patch, MagicMock

from src.tasks import get_file_from_bucket, GoogleStorageError


class TestGetFileFromBucket:
    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch the logger."""
        with patch("src.tasks.get_file_from_bucket.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture
    def mock_settings(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock settings."""
        with patch("src.tasks.get_file_from_bucket.Settings") as mock_settings:
            mock_settings.return_value.bucket_name = "test-bucket"
            yield mock_settings

    @pytest.fixture
    def mock_storage_client(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the Google Cloud Storage client."""
        with patch("src.tasks.get_file_from_bucket.storage.Client") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def mock_bucket(
        self,
        mock_storage_client: MagicMock,
    ) -> Generator[MagicMock, None, None]:
        """Fixture to mock the bucket."""
        mock_bucket = MagicMock()
        mock_storage_client.bucket.return_value = mock_bucket
        yield mock_bucket

    @pytest.fixture
    def mock_blob(
        self,
        mock_bucket: MagicMock
    ) -> Generator[MagicMock, None, None]:
        """Fixture to mock the blob."""
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        yield mock_blob

    def test_get_file_from_bucket_success(
        self,
        mock_settings: MagicMock,
        mock_storage_client: MagicMock,
        mock_bucket: MagicMock,
        mock_blob: MagicMock,
        mock_logger: MagicMock
    ):
        """
        Test successful retrieval of a file from the bucket.
        """
        mock_blob.download_as_bytes.return_value = b"test content"

        file_name = "test-file.txt"

        result = get_file_from_bucket(file_name)

        assert isinstance(result, io.BytesIO)
        assert result.read() == b"test content"
        mock_storage_client.bucket.assert_called_once_with(mock_settings.return_value.google_storage_bucket_name)
        mock_bucket.blob.assert_called_once_with(file_name)
        mock_blob.download_as_bytes.assert_called_once()
        mock_logger.info.assert_called_once_with(f"Downloading file '{file_name}' from Google Cloud Storage")

    def test_get_file_from_bucket_error(
        self,
        mock_settings: MagicMock,
        mock_storage_client: MagicMock,
        mock_bucket: MagicMock,
        mock_blob: MagicMock,
        mock_logger: MagicMock
    ):
        """
        Test the behavior when another error occurs during file retrieval.
        """
        mock_blob.download_as_bytes.side_effect = Exception("Unexpected error")

        file_name = "test-file.txt"

        with pytest.raises(GoogleStorageError, match="Failed to download file from Google Cloud Storage: Unexpected error"):
            get_file_from_bucket(file_name)

        mock_storage_client.bucket.assert_called_once_with(mock_settings.return_value.google_storage_bucket_name)
        mock_bucket.blob.assert_called_once_with(file_name)
        mock_blob.download_as_bytes.assert_called_once()
        mock_logger.info.assert_called_once_with(f"Downloading file '{file_name}' from Google Cloud Storage")
