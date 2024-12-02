from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks import extract_summary_and_keywords


class ExtractSummaryAndKeywords:
    def __call__(self, state: PipelineState) -> Any:
        try:
            return {"state": {"summary": extract_summary_and_keywords(state["state"]["text"])}}
        except Exception as e:
            raise GraphError(e)
