from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks.extract_key_research_findings_and_methodology import extract_key_research_findings_and_methodology


class ExtractKeyResearchFindingsAndMethodology:
    def __call__(self, state: PipelineState) -> Any:
        try:
            return {"state": {"research": extract_key_research_findings_and_methodology(state["state"]["text"])}}
        except Exception as e:
            raise GraphError(e)
