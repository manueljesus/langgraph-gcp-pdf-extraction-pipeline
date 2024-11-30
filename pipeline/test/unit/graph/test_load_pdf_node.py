import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import LoadPDF


class TestLoadPDFNode:
    @pytest.fixture()
    def mock_extract_text_from_pdf(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.load_pdf_node.extract_text_from_pdf", return_value="Mocked extracted text") as mock:
            yield mock

    def test_load_pdf_state(
        self,
        mock_extract_text_from_pdf: MagicMock,
    ) -> None:
        """Test LoadPDF to verify the state output."""
        file = "dummy"
        load_pdf = LoadPDF(file)

        result = load_pdf({"state": {}})

        mock_extract_text_from_pdf.assert_called_once_with(file)
        assert result == {"state": {"text": "Mocked extracted text"}}
