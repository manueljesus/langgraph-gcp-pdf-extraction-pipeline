import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import ExtractKeyResearchFindingsAndMethodology, PipelineState, GraphError


class TestExtractKeyResearchFindingsAndMethodologyNode:
    @pytest.fixture()
    def mock_extract_key_research_findings_and_methodology_task(self) -> Generator[MagicMock, None, None]:
        with patch(
                "src.graph.extract_key_research_findings_and_methodology_node.extract_key_research_findings_and_methodology",
                return_value={"key_findings": ["Finding 1", "Finding 2"], "methodology": "Experimental"}
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
    def extract_key_research_findings_and_methodology(self) -> ExtractKeyResearchFindingsAndMethodology:
        return ExtractKeyResearchFindingsAndMethodology()

    def test_extract_key_research_findings_and_methodology(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_key_research_findings_and_methodology_task: MagicMock,
        extract_key_research_findings_and_methodology: ExtractKeyResearchFindingsAndMethodology
    ) -> None:
        """Test ExtractKeyResearchFindingsAndMethodology node to verify the state output."""
        result = extract_key_research_findings_and_methodology(mock_pipeline_state)

        mock_extract_key_research_findings_and_methodology_task.assert_called_once_with("Mocked extracted text")
        assert result == {
            "state": {
                "research": {"key_findings": ["Finding 1", "Finding 2"], "methodology": "Experimental"}
            }
        }

    def test_extract_key_research_findings_and_methodology_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        extract_key_research_findings_and_methodology: ExtractKeyResearchFindingsAndMethodology
    ) -> None:
        """Test ExtractKeyResearchFindingsAndMethodology raises GraphError on exception."""
        with pytest.raises(GraphError):
            extract_key_research_findings_and_methodology(mock_pipeline_state_with_error)
