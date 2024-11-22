import pytest
import os
from src.utils.hash import generate_file_hash, generate_unique_hash, HashError

class TestHashFunctions:
    """Unit tests for hash utils."""

    # Setup and teardown for test files
    @classmethod
    def setup_class(cls):
        cls.test_file_path = "test_file.txt"
        with open(cls.test_file_path, "w") as f:
            f.write("This is a test file.")

    @classmethod
    def teardown_class(cls):
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

    # Test generate_file_hash
    def test_generate_file_hash_success(self):
        """Test successful file hash generation."""
        hash_value = generate_file_hash(self.test_file_path)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length

    def test_generate_file_hash_file_not_found(self):
        """Test file hash generation with a non-existent file."""
        with pytest.raises(HashError) as excinfo:
            generate_file_hash("non_existent_file.txt")
        assert "File not found" in str(excinfo.value)

    def test_generate_file_hash_read_error(self, monkeypatch):
        """Test file hash generation with a read error."""
        def mock_open(*args, **kwargs):
            raise IOError("Mocked read error")

        monkeypatch.setattr("builtins.open", mock_open)
        with pytest.raises(HashError) as excinfo:
            generate_file_hash(self.test_file_path)
        assert "An error occurred while reading the file" in str(excinfo.value)

    # Test generate_unique_hash
    def test_generate_unique_hash_success(self):
        """Test successful string hash generation."""
        hash_value = generate_unique_hash("Test string")
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length

    def test_generate_unique_hash_empty_string(self):
        """Test string hash generation with an empty string."""
        with pytest.raises(HashError) as excinfo:
            generate_unique_hash("")
        assert "Input string must not be empty" in str(excinfo.value)

    def test_generate_unique_hash_whitespace_string(self):
        """Test string hash generation with a string of only whitespace."""
        with pytest.raises(HashError) as excinfo:
            generate_unique_hash("   ")
        assert "Input string must not be empty" in str(excinfo.value)

