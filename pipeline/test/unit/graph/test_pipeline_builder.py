import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from langgraph.graph.state import CompiledStateGraph
from src.graph import PipelineBuilder, PipelineState

class TestPipelineBuilder:
    """
    Test suite for the PipelineBuilder class.
    """

    @pytest.fixture
    def mock_file(self) -> BytesIO:
        """
        Fixture to provide a mock file (BytesIO).
        """
        return BytesIO(b"Mock PDF content")

    @pytest.fixture
    def paper_id(self) -> str:
        """
        Fixture to provide a mock paper ID.
        """
        return "mock-paper-id"

    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        """
        Fixture to provide a mock pipeline state.
        """
        return {"state": {"processed": False, "final": "state"}}

    @pytest.fixture
    def pipeline_builder(self) -> PipelineBuilder:
        """
        Fixture to instantiate the PipelineBuilder with mock dependencies.
        """
        return PipelineBuilder(file='file.pdf')

    @patch("src.graph.get_file_node.get_file_from_bucket")
    @patch("src.graph.check_processed_paper_node.check_processed_paper")
    def test_pipeline_structure(
        self,
        mock_check_processed_paper: MagicMock,
        mock_get_file: MagicMock,
        pipeline_builder: PipelineBuilder,
    ):
        """
        Test that the pipeline is constructed with the correct nodes and edges.
        """
        mock_check_processed_paper.return_value = {"state": {"processed": False}}
        mock_get_file.return_value = BytesIO(b"Mock file content")

        # Compile the pipeline
        compiled_pipeline = pipeline_builder()

        # Validate the pipeline is compiled successfully
        assert compiled_pipeline is not None
        assert isinstance(compiled_pipeline, CompiledStateGraph)

        # Extract the graph structure
        graph = compiled_pipeline.get_graph()

        # Validate nodes
        expected_nodes = {
            "Get File",
            "Check Processed Paper",
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
            ("__start__", "Get File"),
            ("Get File", "Check Processed Paper"),
            ("Check Processed Paper", "__end__"),  # Conditional edge
            ("Check Processed Paper", "Load PDF"),  # Conditional edge
            ("Load PDF", "Extract Metadata"),
            ("Load PDF", "Extract Key Research Findings And Methodology"),
            ("Load PDF", "Extract Summary And Keywords"),
            ("Extract Metadata", "Merge Results"),
            ("Extract Key Research Findings And Methodology", "Merge Results"),
            ("Extract Summary And Keywords", "Merge Results"),
            ("Merge Results", "Insert Data Into BigQuery"),
            ("Insert Data Into BigQuery", "__end__"),
        }
        actual_edges = {(edge.source, edge.target) for edge in graph.edges}
        assert actual_edges == expected_edges

    @patch("src.graph.get_file_node.get_file_from_bucket")
    @patch("src.graph.check_processed_paper_node.check_processed_paper")
    def test_pipeline_execution_end_path(
        self,
        mock_check_processed_paper: MagicMock,
        mock_get_file: MagicMock,
        mock_pipeline_state: PipelineState,
        pipeline_builder: PipelineBuilder,
    ):
        """
        Test that the pipeline ends early when the paper is already processed.
        """
        # Mock state indicating the paper is already processed
        mock_check_processed_paper.return_value = True
        mock_get_file.return_value = BytesIO(b"Mock file content")

        # Compile and execute the pipeline
        pipeline = pipeline_builder()
        result = pipeline.invoke({"state": {"processed": True}})

        # Assert that the pipeline terminates early
        assert result["state"]["processed"]

    @patch("src.graph.get_file_node.get_file_from_bucket")
    @patch("src.graph.get_file_node.generate_file_hash")
    @patch("src.graph.check_processed_paper_node.check_processed_paper")
    @patch("src.tasks.insert_data_into_bigquery.Settings")
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
        mock_settings: MagicMock,
        mock_check_processed_paper: MagicMock,
        mock_file_hash: MagicMock,
        mock_get_file: MagicMock,
        mock_file: BytesIO,
        paper_id: str,
        mock_pipeline_state: PipelineState,
        pipeline_builder: PipelineBuilder,
    ):
        """
        Test that the pipeline executes all nodes as expected.
        """
        # Set up mock return values
        mock_load_pdf.return_value = mock_pipeline_state
        mock_extract_metadata.return_value = mock_pipeline_state
        mock_extract_key_research.return_value = mock_pipeline_state
        mock_extract_summary_keywords.return_value = mock_pipeline_state
        mock_merge_results.return_value = mock_pipeline_state
        mock_insert_data_bigquery.return_value = mock_pipeline_state
        mock_settings.return_value.bigquery_dataset_id = "test_dataset"
        mock_settings.return_value.bucket_name = "test_bucket"
        mock_check_processed_paper.return_value = False
        mock_get_file.return_value = mock_file
        mock_file_hash.return_value = paper_id

        expected_state = {
            "state": {
                "file": mock_file,
                "paper_id": paper_id,
                "processed": False,
                "final": "state"
            }
        }

        # Compile and execute the pipeline
        pipeline = pipeline_builder()
        result = pipeline.invoke({"state": {}})

        # Validate that all nodes were called
        mock_load_pdf.assert_called_once()
        mock_extract_metadata.assert_called_once()
        mock_extract_key_research.assert_called_once()
        mock_extract_summary_keywords.assert_called_once()
        mock_merge_results.assert_called_once()
        mock_insert_data_bigquery.assert_called_once()

        # Validate the final state
        assert result == expected_state

