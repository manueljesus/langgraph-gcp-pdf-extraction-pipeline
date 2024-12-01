import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from typing import Generator
from langgraph.graph.state import CompiledStateGraph
from google.cloud.bigquery import Client as BigQueryClient

from src.graph import PipelineBuilder, PipelineState


class TestPipelineBuilder:
    """
    Pipeline PipelineBuilder test suite.
    """

    @pytest.fixture
    def mock_file(self) -> BytesIO:
        """
        Fixture to provide a mock file (BytesIO).
        """
        return BytesIO(b"Mock PDF content")

    @pytest.fixture
    def mock_bigquery_client(self) -> MagicMock:
        """Fixture to create a mock BigQuery client."""
        client = MagicMock(spec=BigQueryClient)
        client.project_id = "test_project"
        return client

    @pytest.fixture
    def paper_id(self) -> StopAsyncIteration:
        """
        Paper ID
        """
        return "mock-paper-id"

    @pytest.fixture()
    def mock_extract_text_from_pdf_task(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.load_pdf_node.extract_text_from_pdf", return_value="Mocked extracted text") as mock:
            yield mock

    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        return {"state": {"final": "state"}}

    @pytest.fixture
    def pipeline_builder(
        self,
        mock_file: BytesIO,
        paper_id: str,
        mock_bigquery_client: BigQueryClient
    ) -> PipelineBuilder:
        """
        PipelineBuilder with mock dependencies.
        """
        return PipelineBuilder(
            file=mock_file,
            paper_id=paper_id,
            bigquery_client=mock_bigquery_client
        )

    def test_pipeline_structure(
        self,
        pipeline_builder: PipelineBuilder
    ):
        """
        Test that the pipeline is constructed with the correct nodes and edges.
        """
        compiled_pipeline = pipeline_builder()

        # Verify that the pipeline is compiled
        assert compiled_pipeline is not None and isinstance(compiled_pipeline, CompiledStateGraph)

        # Extract the graph structure to validate nodes and edges
        graph = compiled_pipeline.get_graph()

        # Validate nodes
        expected_nodes = {
            "Load PDF",
            "Extract Metadata",
            "Extract Key Research Findings And Methodology",
            "Extract Summary And Keywords",
            "Merge Results",
            "Insert Data Into BigQuery",
        }
        assert set(graph.nodes) == expected_nodes | {"__start__", "__end__"}

        # Validate edges
        expected_edges = {
            ("__start__", "Load PDF"),
            ("Load PDF", "Extract Metadata"),
            ("Load PDF", "Extract Key Research Findings And Methodology"),
            ("Load PDF", "Extract Summary And Keywords"),
            ("Extract Metadata", "Merge Results"),
            ("Extract Key Research Findings And Methodology", "Merge Results"),
            ("Extract Summary And Keywords", "Merge Results"),
            ("Merge Results", "Insert Data Into BigQuery"),
            ("Insert Data Into BigQuery", "__end__"),
        }
        assert {(edge.source, edge.target) for edge in graph.edges} == expected_edges

    @patch("src.tasks.insert_data_into_bigquery.get_settings")
    @patch("src.graph.insert_data_into_bigquery_node.InsertDataIntoBigQuery.__call__")
    @patch("src.graph.merge_results_node.MergeResults.__call__")
    @patch("src.graph.extract_summary_and_keywords_node.ExtractSummaryAndKeywords.__call__")
    @patch("src.graph.extract_key_research_findings_and_methodology_node.ExtractKeyResearchFindingsAndMethodology.__call__")
    @patch("src.graph.extract_metadata_node.ExtractMetadata.__call__")
    @patch("src.graph.load_pdf_node.LoadPDF.__call__")
    def test_pipeline_execution(
        self,
        mock_load_pdf: MagicMock,
        mock_extract_metadata: MagicMock,
        mock_extract_key_research: MagicMock,
        mock_extract_summary_keywords: MagicMock,
        mock_merge_results: MagicMock,
        mock_insert_data_bigquery: MagicMock,
        mock_get_settings: MagicMock,
        mock_pipeline_state: PipelineState,
        pipeline_builder: PipelineBuilder,
        mock_extract_text_from_pdf_task: MagicMock,
        mock_bigquery_client: MagicMock
    ):
        """
        Test that the pipeline executes as expected.
        """
        # Mock each node to return a modified state
        mock_load_pdf.return_value = mock_pipeline_state
        mock_extract_metadata.return_value = mock_pipeline_state
        mock_extract_key_research.return_value = mock_pipeline_state
        mock_extract_summary_keywords.return_value = mock_pipeline_state
        mock_merge_results.return_value = mock_pipeline_state
        mock_insert_data_bigquery.return_value = mock_pipeline_state
        mock_get_settings.return_value.bigquery_dataset_id = "test_dataset"

        # Build the pipeline
        pipeline = pipeline_builder()

        # Execute the pipeline
        result = pipeline.invoke({"state": {}})

        # Assert that all mock nodes were called
        mock_load_pdf.assert_called_once()
        mock_extract_metadata.assert_called_once()
        mock_extract_key_research.assert_called_once()
        mock_extract_summary_keywords.assert_called_once()
        mock_merge_results.assert_called_once()
        mock_insert_data_bigquery.assert_called_once()

        # Ensure the final state is returned
        # The state is overridden in each node to be the same, so this is expected
        assert result == mock_pipeline_state
