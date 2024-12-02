from typing import Any, Union
from io import BytesIO
from src.graph import PipelineState, GraphError
from src.tasks import check_processed_paper


class CheckProcessedPaper:
    def __call__(self, state: PipelineState) -> bool:
        try:
            return check_processed_paper(state["state"]["paper_id"])
        except Exception as e:
            raise GraphError(e)
