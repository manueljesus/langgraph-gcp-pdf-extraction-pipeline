import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch
from src.utils.pdf_utils import extract_text_from_pdf, PDFExtractionError

@patch('pdfplumber.open')
def test_extract_text_from_pdf(
    mock_pdfplumber_open: MagicMock
):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()

    mock_page1.extract_text.return_value = "Page 1 text."
    mock_page2.extract_text.return_value = "Page 2 text."

    # Mocking pdf.pages
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

    pdf_path = "dummy_path.pdf"
    result = extract_text_from_pdf(pdf_path)

    # Asserting the result
    assert result == "Page 1 text.Page 2 text."

@patch('pdfplumber.open')
def test_extract_text_from_pdf_empty(
    mock_pdfplumber_open: MagicMock
):
    mock_pdf = MagicMock()
    mock_pdf.pages = []
    mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

    # Running the test
    pdf_path = "dummy_path.pdf"
    result = extract_text_from_pdf(pdf_path)

    # Asserting the result
    assert result == ""

@patch('pdfplumber.open')
def test_extract_text_from_pdf_error(
    mock_pdfplumber_open: MagicMock
):
    # Mocking pdfplumber to raise an exception
    mock_pdfplumber_open.side_effect = Exception("File not found")

    # Running the test and expecting a custom exception
    pdf_path = "non_existent.pdf"
    with pytest.raises(PDFExtractionError, match="Failed to extract text from PDF: File not found"):
        extract_text_from_pdf(pdf_path)

@patch('pdfplumber.open')
def test_extract_text_from_pdf_bytesio(
    mock_pdfplumber_open: MagicMock
):
    mock_pdf = MagicMock()
    mock_page1 = MagicMock()
    mock_page2 = MagicMock()

    mock_page1.extract_text.return_value = "Page 1 text."
    mock_page2.extract_text.return_value = "Page 2 text."

    # Mocking pdf.pages
    mock_pdf.pages = [mock_page1, mock_page2]
    mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

    # Creating a BytesIO object
    pdf_bytes = BytesIO(b"%PDF-1.4 dummy pdf content")

    # Running the test
    result = extract_text_from_pdf(pdf_bytes)

    # Asserting the result
    assert result == "Page 1 text.Page 2 text."
