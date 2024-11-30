from typing import Any, Union
from io import BytesIO
from src.graph import PipelineState
from src.utils.pdf_utils import extract_text_from_pdf


class LoadPDF:
    def __init__(self, file: Union[str, BytesIO]):
        self.file = file

    def __call__(self, _: PipelineState) -> Any:
        return {"state": {"text": extract_text_from_pdf(self.file)}}
