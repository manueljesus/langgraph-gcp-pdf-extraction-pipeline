import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import LoadPDF, PipelineState


class TestLoadPDFNode:
    @pytest.fixture()
    def mock_extract_text_from_pdf_task(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.load_pdf_node.extract_text_from_pdf", return_value="Mocked extracted text") as mock:
            yield mock

    @pytest.fixture()
    def file(self) -> str:
        return "dummy"

    @pytest.fixture()
    def mock_pipeline_state(
        self,
        file: str
    ) -> PipelineState:
        return {
            "state": {"file": file}
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {}  # No "file" key to trigger an error
        }

    @pytest.fixture()
    def load_pdf(self) -> LoadPDF:
        return LoadPDF()

    def test_load_pdf_state(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_text_from_pdf_task: MagicMock,
        file: str,
        load_pdf: LoadPDF
    ) -> None:
        """Test LoadPDF to verify the state output."""
        result = load_pdf(mock_pipeline_state)

        mock_extract_text_from_pdf_task.assert_called_once_with(file)
        assert result == {"state": {"text": "Mocked extracted text"}}

    def test_load_pdf_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        load_pdf: LoadPDF
    ) -> None:
        """Test LoadPDF raises GraphError on exception."""
        with pytest.raises(Exception):
            load_pdf(mock_pipeline_state_with_error)
