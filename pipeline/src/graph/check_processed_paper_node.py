from src.graph import PipelineState, GraphError
from src.tasks import check_processed_paper

from src.logger import get_logger

logger = get_logger(__name__)


class CheckProcessedPaper:
    def __call__(self, state: PipelineState) -> bool:
        try:
            logger.info(f"Checking if paper ID {state.get('state', {}).get('paper_id', None)} has been processed")
            return {"state": {"processed": check_processed_paper(state["state"]["paper_id"])}}
        except Exception as e:
            logger.error(f"Failed to check if paper ID {state.get('state', {}).get('paper_id', None)} has been processed: {e}")
            raise GraphError(e)
