from typing import Annotated, TypedDict, Dict, Any


def update_state(
    a: Dict[str, Any],
    b: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge two dictionaries `a` and `b` into a new dictionary.

    Args:
        a: The first dictionary.
        b: The second dictionary.

    Returns:
        A new dictionary containing the merged content of `a` and `b`.
    """
    updated = a.copy()
    updated.update(b)

    return updated


class PipelineState(TypedDict):
    """
    Represents the shared state object used by pipeline nodes in a data processing workflow.

    The `PipelineState` is a structured dictionary that serves as a shared state for the pipeline.
    Each node reads from and updates this shared state, ensuring a seamless flow of data throughout the pipeline.

    Attributes:
        state (Annotated[Dict[str, Any], update_state]):
            A dictionary designed for additive operations, where new data from pipeline nodes
            is merged or updated. the `update_state` function is the reduce function to 
            update the state, by merging the new dictionary output from the just-executed node
            to the current shared state two dictionaries.

    Usage:
        This object is initialized as:

        >>> state: PipelineState = {"state": {}}

        Pipeline nodes are expected to return a dictionary with the new data to be merged into the state:
        >>> return {'state': {'key': 'value'}}

        - This structure ensures the state maintains a single dictionary for downstream operations.
    """
    state: Annotated[Dict[str, Any], update_state]
