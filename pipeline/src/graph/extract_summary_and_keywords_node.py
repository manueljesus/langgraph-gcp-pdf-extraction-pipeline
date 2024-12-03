from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks import extract_summary_and_keywords
from src.logger import get_logger

logger = get_logger(__name__)


class ExtractSummaryAndKeywords:
    def __call__(self, state: PipelineState) -> Any:
        try:
            logger.info(f"Extracting summary and keywords from paper ID {state.get('state', {}).get('paper_id', None)}")
            return {"state": {"summary": extract_summary_and_keywords(state["state"]["text"])}}
        except Exception as e:
            logger.error(f"Failed to extract summary and keywords from paper ID {state.get('state', {}).get('paper_id', None)}: {e}")
            raise GraphError(e)
