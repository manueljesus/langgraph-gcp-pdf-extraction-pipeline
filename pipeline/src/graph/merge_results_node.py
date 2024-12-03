from typing import Any
from functools import reduce
from src.graph import PipelineState, GraphError
from src.logger import get_logger

logger = get_logger(__name__)


class MergeResults:
    """
    Merge the results from the pipeline state into a single dictionary,
    excluding the 'text' key.

    This node flattens the state by merging all keys which are dictionaries into a single dictionary.

    In consequence, the shared state is *rewritten* here, since there is no need to keep the previous
    structure.
    """
    def __call__(self, state: PipelineState) -> Any:
        try:
            logger.info(f"Merging results for paper ID {state.get('state', {}).get('paper_id', None)}")
            merged_result = reduce(
                lambda a, b: {**a, **b},
                (
                    value
                    for _, value in state["state"].items()
                    if isinstance(value, dict)
                ),
                {}
            )

            return {"state": {**merged_result}}

        except Exception as e:
            logger.error(f"Failed to merge results.")
            raise GraphError(e)
