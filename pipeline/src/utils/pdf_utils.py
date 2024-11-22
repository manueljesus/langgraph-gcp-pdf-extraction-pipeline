import pdfplumber
from io import BytesIO
from typing import Union

class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""
    pass

def extract_text_from_pdf(pdf: Union[str, BytesIO]) -> str:
    """Extract text from a PDF file using pdfplumber.

    Args:
        pdf (Union[str, BytesIO]): Path to the PDF file or a BytesIO object.

    Returns:
        str: Text extracted from the PDF file.

    Raises:
        PDFExtractionError: If the PDF cannot be opened or processed.
    """
    try:
        with pdfplumber.open(pdf) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
        return text
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract text from PDF: {e}")
