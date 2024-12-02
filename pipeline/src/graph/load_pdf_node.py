from typing import Any, Union
from io import BytesIO
from src.graph import PipelineState, GraphError
from src.utils.pdf_utils import extract_text_from_pdf


class LoadPDF:
    def __call__(self, state: PipelineState) -> Any:
        try:
            return {"state": {"text": extract_text_from_pdf(state['state']['file'])}}
        except Exception as e:
            raise GraphError(e)
