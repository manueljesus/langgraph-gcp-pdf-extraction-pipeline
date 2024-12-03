import pytest
import os
from io import BytesIO
from typing import Union, Generator
from unittest.mock import patch, MagicMock
from src.utils.hash import generate_file_hash, generate_unique_hash, HashError


@pytest.fixture
def mock_logger() -> Generator[MagicMock, None, None]:
    """
    Fixture to patch the logger and provide a mock logger instance.
    """
    with patch("src.utils.hash.logger") as mock_logger:
        yield mock_logger


class TestFileHash:
    """Unit tests for generate_file_hash."""

    # Setup and teardown for test files
    @classmethod
    def setup_class(cls):
        cls.test_file_path = "test_file.txt"
        cls.test_file_content = "This is a test file."
        with open(cls.test_file_path, "w") as f:
            f.write(cls.test_file_content)

    @classmethod
    def teardown_class(cls):
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

    @pytest.mark.parametrize(
        "file_input",
        [
            pytest.param("test_file.txt"),
            pytest.param(BytesIO("This is a test file.".encode("utf-8"))),
        ],
    )
    def test_generate_file_hash_success(
        self,
        file_input: Union[str, BytesIO],
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test successful file hash generation for both file path and file-like object."""
        hash_value = generate_file_hash(file_input)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length
        # Verify logging calls
        mock_logger.info.assert_any_call(f"Generating hash for file: {file_input}")
        mock_logger.info.assert_any_call(f"Hash generated: {hash_value}")

    def test_generate_file_hash_non_existent_file(
        self,
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test file hash generation with a non-existent file."""
        with pytest.raises(FileNotFoundError):
            generate_file_hash("non_existent_file.txt")
        # Verify logging call
        mock_logger.info.assert_any_call("Generating hash for file: non_existent_file.txt")

    @pytest.mark.parametrize(
        "file_input",
        [
            pytest.param(BytesIO()),
            pytest.param("test_empty_file.txt"),
        ],
    )
    def test_generate_file_hash_empty(
        self,
        file_input: Union[str, BytesIO],
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test file hash generation with an empty file or file-like object."""
        if isinstance(file_input, str):
            # Create an empty file
            with open(file_input, "w"):
                pass
        try:
            hash_value = generate_file_hash(file_input)
            assert isinstance(hash_value, str)
            assert len(hash_value) == 64  # SHA-256 hash length
            # Verify logging calls
            mock_logger.info.assert_any_call(f"Generating hash for file: {file_input}")
            mock_logger.info.assert_any_call(f"Hash generated: {hash_value}")
        finally:
            if isinstance(file_input, str) and os.path.exists(file_input):
                os.remove(file_input)

    def test_generate_file_hash_read_error(
        self,
        monkeypatch,
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test file hash generation with a read error."""
        def mock_open(*args, **kwargs):
            raise IOError("Mocked read error")

        monkeypatch.setattr("builtins.open", mock_open)
        with pytest.raises(OSError):
            generate_file_hash(self.test_file_path)
        # Verify logging call
        mock_logger.info.assert_any_call(f"Generating hash for file: {self.test_file_path}")


class TestUniqueHash:
    """Unit tests for generate_unique_hash."""

    def test_generate_unique_hash_success(
        self,
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test successful string hash generation."""
        hash_value = generate_unique_hash("Test string")
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length
        # Verify logging calls
        mock_logger.info.assert_any_call("Generating hash for string: Test string")
        mock_logger.info.assert_any_call(f"Hash generated: {hash_value}")

    def test_generate_unique_hash_empty_string(
        self,
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test string hash generation with an empty string."""
        with pytest.raises(HashError) as excinfo:
            generate_unique_hash("")
        assert "Input string must not be empty" in str(excinfo.value)
        # Verify logging calls
        mock_logger.info.assert_any_call("Generating hash for string: ")
        mock_logger.error.assert_any_call("Input string must not be empty or only whitespace.")

    def test_generate_unique_hash_whitespace_string(
        self,
        mock_logger: Generator[MagicMock, None, None]
    ):
        """Test string hash generation with a string of only whitespace."""
        with pytest.raises(HashError) as excinfo:
            generate_unique_hash("   ")
        assert "Input string must not be empty" in str(excinfo.value)
        # Verify logging calls
        mock_logger.info.assert_any_call("Generating hash for string:    ")
        mock_logger.error.assert_any_call("Input string must not be empty or only whitespace.")
