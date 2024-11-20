import pdfplumber

class PDFExtractionError(Exception):
    """Custom exception for PDF extraction errors."""
    pass

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using pdfplumber.

    Args:
        pdf_path (str): PDF file path.

    Returns:
        str: Text extracted from the PDF file.

    Raises:
        PDFExtractionError: If the PDF cannot be opened or processed.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
        return text
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract text from PDF: {e}")
