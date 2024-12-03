import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import LoadPDF, PipelineState, GraphError


class TestLoadPDFNode:
    @pytest.fixture()
    def mock_extract_text_from_pdf_task(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.load_pdf_node.extract_text_from_pdf", return_value="Mocked extracted text") as mock:
            yield mock

    @pytest.fixture()
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.load_pdf_node.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture()
    def file(self) -> str:
        return "dummy"

    @pytest.fixture()
    def mock_pipeline_state(
        self,
        file: str
    ) -> PipelineState:
        return {
            "state": {
                "file": file,
                "paper_id": "paper_id"
            }
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {"paper_id": "paper_id"}  # Missing "file" key to trigger an error
        }

    @pytest.fixture()
    def load_pdf(self) -> LoadPDF:
        return LoadPDF()

    def test_load_pdf_state(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_text_from_pdf_task: MagicMock,
        mock_logger: MagicMock,
        file: str,
        load_pdf: LoadPDF
    ) -> None:
        """Test LoadPDF to verify the state output."""
        result = load_pdf(mock_pipeline_state)

        mock_extract_text_from_pdf_task.assert_called_once_with(file)
        mock_logger.info.assert_called_once_with("Extracting text from PDF for paper ID paper_id")
        assert result == {"state": {"text": "Mocked extracted text"}}

    def test_load_pdf_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        mock_logger: MagicMock,
        load_pdf: LoadPDF
    ) -> None:
        """Test LoadPDF raises GraphError on exception."""
        with pytest.raises(GraphError):
            load_pdf(mock_pipeline_state_with_error)
        mock_logger.error.assert_called_once_with(
            "Failed to extract text from PDF for paper ID paper_id: 'file'"
        )
