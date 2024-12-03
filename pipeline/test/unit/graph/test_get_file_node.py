import pytest
from unittest.mock import patch, MagicMock
from typing import Generator
from io import BytesIO
from src.graph import GetFile


class TestGetFileNode:
    @pytest.fixture()
    def mock_file(self) -> BytesIO:
        return BytesIO(b"Mocked file content")

    @pytest.fixture()
    def mock_get_file_from_bucket(
        self,
        mock_file: BytesIO
    ) -> Generator[MagicMock, None, None]:
        with patch("src.graph.get_file_node.get_file_from_bucket", return_value=mock_file) as mock:
            yield mock

    @pytest.fixture()
    def mock_generate_file_hash(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.get_file_node.generate_file_hash", return_value="mocked_paper_id") as mock:
            yield mock

    @pytest.fixture()
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.get_file_node.logger") as mock_logger:
            yield mock_logger

    def test_get_file_state(
        self,
        mock_file: BytesIO,
        mock_get_file_from_bucket: MagicMock,
        mock_generate_file_hash: MagicMock,
        mock_logger: MagicMock,
    ) -> None:
        """Test GetFile to verify the state output."""
        file_name = "dummy_file.pdf"
        get_file_node = GetFile(file_name)

        result = get_file_node({"state": {}})

        mock_get_file_from_bucket.assert_called_once_with(file_name)
        mock_generate_file_hash.assert_called_once_with(mock_file)
        mock_logger.info.assert_called_once_with(f"Getting file {file_name} from GCS bucket")

        assert result == {
            "state": {
                "file": mock_file,
                "paper_id": "mocked_paper_id"
            }
        }
