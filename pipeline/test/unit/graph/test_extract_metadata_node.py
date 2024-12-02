import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import ExtractMetadata, PipelineState, GraphError


class TestExtractMetadataNode:
    @pytest.fixture()
    def mock_extract_metadata_task(self) -> Generator[MagicMock, None, None]:
        with patch(
            "src.graph.extract_metadata_node.extract_metadata",
            return_value="metadata"
        ) as mock:
            yield mock

    @pytest.fixture()
    def mock_pipeline_state(self) -> PipelineState:
        return {
            "state": {"text": "Mocked extracted text"}
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {}  # No "text" key to trigger an error
        }

    @pytest.fixture()
    def extract_metadata(self) -> ExtractMetadata:
        return ExtractMetadata()

    def test_extract_metadata(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_metadata_task: MagicMock,
        extract_metadata: ExtractMetadata
    ) -> None:
        """Test ExtractMetadata node to verify the state output."""
        result = extract_metadata(mock_pipeline_state)

        mock_extract_metadata_task.assert_called_once_with("Mocked extracted text")
        assert result == {
            "state": {
                "metadata": "metadata"
            }
        }

    def test_extract_metadata_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        extract_metadata: ExtractMetadata
    ) -> None:
        """Test ExtractMetadata raises GraphError on exception."""
        with pytest.raises(GraphError):
            extract_metadata(mock_pipeline_state_with_error)
