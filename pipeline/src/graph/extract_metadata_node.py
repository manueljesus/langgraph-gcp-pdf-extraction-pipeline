from src.graph import PipelineState, GraphError
from typing import Any
from src.tasks import extract_metadata
from src.logger import get_logger

logger = get_logger(__name__)


class ExtractMetadata:
    def __call__(self, state: PipelineState) -> Any:
        try:
            logger.info(f"Extracting metadata from paper ID {state.get('state', {}).get('paper_id', None)}")
            return {"state": {"metadata": extract_metadata(state["state"]["text"])}}
        except Exception as e:
            logger.error(f"Failed to extract metadata from paper ID {state.get('state', {}).get('paper_id', None)}: {e}")
            raise GraphError(e)
