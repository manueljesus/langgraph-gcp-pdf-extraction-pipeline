import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from src.graph import PipelineState, GraphError, InsertDataIntoBigQuery


class TestInsertDataIntoBigQueryNode:
    @pytest.fixture()
    def mock_insert_data_into_bigquery_task(self) -> Generator[MagicMock, None, None]:
        with patch(
            "src.graph.insert_data_into_bigquery_node.insert_data_into_bigquery"
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        """
        Fixture to provide a mock PipelineState with appropriate state data.
        """
        return {
            "state":
                {
                    "text": "text",
                    "title": "title",
                    "authors": "authors",
                    "abstract": "abstract",
                    "publication_date": "publication_date",
                    "summary": "summary",
                    "keywords": "keywords",
                    "methodology": "methodology",
                    "key_research_findings": "key_research_findings"
                }
        }

    @pytest.fixture
    def mock_bigquery_client(
        self
    ) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def insert_data_into_bigquery(
        self,
        mock_bigquery_client: MagicMock
    ) -> InsertDataIntoBigQuery:
        return InsertDataIntoBigQuery(
            mock_bigquery_client,
            "paper_id"
        )

    def test_insert_data_into_bigquery(
            self,
            mock_pipeline_state: PipelineState,
            mock_insert_data_into_bigquery_task: MagicMock,
            mock_bigquery_client: MagicMock,
            insert_data_into_bigquery: InsertDataIntoBigQuery
    ) -> None:
        """
        Test InsertDataIntoBigQuery node to verify data is correctly sent into BigQuery client.
        """
        result = insert_data_into_bigquery(mock_pipeline_state)

        mock_insert_data_into_bigquery_task.assert_called_once_with(
            mock_bigquery_client,
            "paper_id",
            {
                "title": "title",
                "authors": "authors",
                "abstract": "abstract",
                "publication_date": "publication_date",
                "summary": "summary",
                "keywords": "keywords",
                "methodology": "methodology",
                "key_research_findings": "key_research_findings"
            }
        )

        assert result == {"state": {}}

    def test_insert_data_into_bigquery_raises_error(
        self,
        mock_pipeline_state: PipelineState,
        mock_insert_data_into_bigquery_task: MagicMock,
        insert_data_into_bigquery: InsertDataIntoBigQuery
    ) -> None:
        """Test ExtractSummaryAndKeywords raises GraphError on exception."""
        mock_insert_data_into_bigquery_task.side_effect = Exception("Mocked exception")

        with pytest.raises(GraphError):
            insert_data_into_bigquery(mock_pipeline_state)