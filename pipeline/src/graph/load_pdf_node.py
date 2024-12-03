from typing import Any, Union
from io import BytesIO
from src.graph import PipelineState, GraphError
from src.utils.pdf_utils import extract_text_from_pdf
from src.logger import get_logger

logger = get_logger(__name__)


class LoadPDF:
    def __call__(self, state: PipelineState) -> Any:
        try:
            logger.info(f"Extracting text from PDF for paper ID {state.get('state', {}).get('paper_id', None)}")
            return {"state": {"text": extract_text_from_pdf(state['state']['file'])}}
        except Exception as e:
            logger.error(f"Failed to extract text from PDF for paper ID {state.get('state', {}).get('paper_id', None)}: {e}")
            raise GraphError(e)
