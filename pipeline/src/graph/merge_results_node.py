from typing import Any
from functools import reduce
from src.graph import PipelineState, GraphError


class MergeResults:
    """
    Merge the results from the pipeline state into a single dictionary,
    excluding the 'text' key.

    This node flattens the state by merging all keys except 'text' into a single
    dictionary.

    In consequence, the shared state is *rewritten* here, since there is no need to keep the previous
    structure.
    """
    def __call__(self, state: PipelineState) -> Any:
        try:
            merged_result = reduce(
                lambda a, b: {**a, **b},
                (
                    value
                    for key, value in state["state"].items()
                    if key != "text"
                ),
                {}
            )

            return {"state": {**merged_result}}

        except Exception as e:
            raise GraphError(e)
