from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks.extract_key_research_findings_and_methodology import extract_key_research_findings_and_methodology
from src.logger import get_logger

logger = get_logger(__name__)


class ExtractKeyResearchFindingsAndMethodology:
    def __call__(self, state: PipelineState) -> Any:
        try:
            logger.info(f"Extracting key research findings and methodology from paper ID {state.get('state', {}).get('paper_id', None)}")
            return {"state": {"research": extract_key_research_findings_and_methodology(state["state"]["text"])}}
        except Exception as e:
            logger.error(f"Failed to extract key research findings and methodology from paper ID {state.get('state', {}).get('paper_id', None)}: {e}")
            raise GraphError(e)
