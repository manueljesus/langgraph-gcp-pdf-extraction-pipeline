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
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.extract_key_research_findings_and_methodology_node.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture()
    def mock_pipeline_state(self) -> PipelineState:
        return {
            "state": {
                "text": "Mocked extracted text",
                "paper_id": "paper_id"
            }
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {
                "paper_id": "paper_id"  # Missing "text" key to trigger an error
            }
        }

    @pytest.fixture()
    def extract_key_research_findings_and_methodology(self) -> ExtractKeyResearchFindingsAndMethodology:
        return ExtractKeyResearchFindingsAndMethodology()

    def test_extract_key_research_findings_and_methodology(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_key_research_findings_and_methodology_task: MagicMock,
        mock_logger: MagicMock,
        extract_key_research_findings_and_methodology: ExtractKeyResearchFindingsAndMethodology
    ) -> None:
        """Test ExtractKeyResearchFindingsAndMethodology node to verify the state output."""
        result = extract_key_research_findings_and_methodology(mock_pipeline_state)

        mock_extract_key_research_findings_and_methodology_task.assert_called_once_with("Mocked extracted text")
        mock_logger.info.assert_called_once_with(
            "Extracting key research findings and methodology from paper ID paper_id"
        )
        assert result == {
            "state": {
                "research": {"key_findings": ["Finding 1", "Finding 2"], "methodology": "Experimental"}
            }
        }

    def test_extract_key_research_findings_and_methodology_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        mock_logger: MagicMock,
        extract_key_research_findings_and_methodology: ExtractKeyResearchFindingsAndMethodology
    ) -> None:
        """Test ExtractKeyResearchFindingsAndMethodology raises GraphError on exception."""
        with pytest.raises(GraphError):
            extract_key_research_findings_and_methodology(mock_pipeline_state_with_error)
        mock_logger.error.assert_called_once_with(
            "Failed to extract key research findings and methodology from paper ID paper_id: 'text'"
        )
