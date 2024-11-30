import pytest
from typing import Dict, Any
from src.graph.pipeline_state import PipelineState, update_state


class TestPipelineState:
    @pytest.fixture
    def state(self) -> PipelineState:
        # Initialize the PipelineState with an empty state
        return {"state": {}}

    def test_initial_state(
        self,
        state: PipelineState
    ) -> None:
        """
        Test that an initial state can be created and is empty.
        """
        assert isinstance(state, dict)
        assert "state" in state
        assert state["state"] == {}

    def test_add_to_state(
        self,
        state: PipelineState
    ) -> None:
        """
        Test that items can be added to the state using the update_state function.
        """
        new_data = {"item1": "Item 1"}
        state["state"] = update_state(state["state"], new_data)

        new_data = {"item2": "Item 2"}
        state["state"] = update_state(state["state"], new_data)

        assert state["state"] == {"item1": "Item 1", "item2": "Item 2"}

    def test_complex_data_structure(
        self,
        state: PipelineState
    ) -> None:
        """
        Test that the state can handle complex nested data structures.
        """
        complex_item = {"key": "value", "nested": [1, 2, 3]}
        new_data = {"complex_item": complex_item}

        state["state"] = update_state(state["state"], new_data)

        assert len(state["state"]) == 1
        assert state["state"]["complex_item"]["key"] == "value"
        assert state["state"]["complex_item"]["nested"] == [1, 2, 3]

    def test_merge_states(
        self,
        state: PipelineState
    ) -> None:
        """
        Test that the state can merge with another state.
        """
        new_data_1 = {"key1": "value1", "key2": "value2"}
        new_data_2 = {"key2": "new_value2", "key3": "value3"}

        state["state"] = update_state(state["state"], new_data_1)
        state["state"] = update_state(state["state"], new_data_2)

        # `key2` should be updated to `new_value2`, and `key3` should be added
        assert state["state"] == {
            "key1": "value1",
            "key2": "new_value2",
            "key3": "value3"
        }
