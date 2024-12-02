from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks import extract_metadata


class ExtractMetadata:
    def __call__(self, state: PipelineState) -> Any:
        try:
            return {"state": {"metadata": extract_metadata(state["state"]["text"])}}
        except Exception as e:
            raise GraphError(e)
