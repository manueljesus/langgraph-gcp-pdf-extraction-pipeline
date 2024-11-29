import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch
from src.utils.pdf_utils import extract_text_from_pdf, PDFExtractionError
from typing import Generator
from unittest.mock import Mock


class TestPDFUtils:
    """
    PDF Utils test suite
    """
    @pytest.fixture
    def mock_pdf_with_pages(self) -> MagicMock:
        """Mocked pdfplumber PDF with pages."""
        mock_pdf = MagicMock()
        mock_page1 = MagicMock()
        mock_page2 = MagicMock()

        mock_page1.extract_text.return_value = "Page 1 text."
        mock_page2.extract_text.return_value = "Page 2 text."

        mock_pdf.pages = [mock_page1, mock_page2]
        return mock_pdf

    @pytest.fixture
    def mock_pdf_empty(self) -> MagicMock:
        """Mocked pdfplumber PDF with no pages."""
        mock_pdf = MagicMock()
        mock_pdf.pages = []
        return mock_pdf

    @pytest.fixture
    def mock_pdfplumber_open(self) -> Generator[Mock, None, None]:
        """Mock pdfplumber.open()"""
        with patch('pdfplumber.open') as mock_pdfplumber_open:
            yield mock_pdfplumber_open

    def test_extract_text_from_pdf(
        self,
        mock_pdf_with_pages: MagicMock,
        mock_pdfplumber_open: MagicMock
    ):
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf_with_pages

        pdf_path = "dummy_path.pdf"
        result = extract_text_from_pdf(pdf_path)

        assert result == "Page 1 text.Page 2 text."

    def test_extract_text_from_pdf_empty(
        self,
        mock_pdf_empty: MagicMock,
        mock_pdfplumber_open: MagicMock
    ):
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf_empty

        pdf_path = "dummy_path.pdf"
        result = extract_text_from_pdf(pdf_path)

        assert result == ""

    def test_extract_text_from_pdf_error(
        self,
        mock_pdfplumber_open: MagicMock
    ):
        # Mocking pdfplumber to raise an exception
        mock_pdfplumber_open.side_effect = Exception("File not found")

        # Running the test and expecting a custom exception
        pdf_path = "non_existent.pdf"
        with pytest.raises(PDFExtractionError, match="Failed to extract text from PDF: File not found"):
            extract_text_from_pdf(pdf_path)

    def test_extract_text_from_pdf_bytesio(
        self,
        mock_pdf_with_pages: MagicMock,
        mock_pdfplumber_open: MagicMock
    ):
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf_with_pages

        # Creating a BytesIO object
        pdf_bytes = BytesIO(b"%PDF-1.4 dummy pdf content")

        result = extract_text_from_pdf(pdf_bytes)

        assert result == "Page 1 text.Page 2 text."
