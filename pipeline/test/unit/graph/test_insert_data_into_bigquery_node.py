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

    @pytest.fixture()
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.insert_data_into_bigquery_node.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        """
        Fixture to provide a mock PipelineState with appropriate state data.
        """
        return {
            "state":
                {
                    "text": "text",
                    "paper_id": "paper_id",
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
    def insert_data_into_bigquery(
        self
    ) -> InsertDataIntoBigQuery:
        return InsertDataIntoBigQuery()

    def test_insert_data_into_bigquery(
            self,
            mock_pipeline_state: PipelineState,
            mock_insert_data_into_bigquery_task: MagicMock,
            mock_logger: MagicMock,
            insert_data_into_bigquery: InsertDataIntoBigQuery
    ) -> None:
        """
        Test InsertDataIntoBigQuery node to verify data is correctly sent into BigQuery client.
        """
        result = insert_data_into_bigquery(mock_pipeline_state)

        mock_insert_data_into_bigquery_task.assert_called_once_with(
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

        mock_logger.info.assert_called_once_with("Inserting data into BigQuery")
        assert result == {"state": {}}

    def test_insert_data_into_bigquery_raises_error(
        self,
        mock_pipeline_state: PipelineState,
        mock_insert_data_into_bigquery_task: MagicMock,
        mock_logger: MagicMock,
        insert_data_into_bigquery: InsertDataIntoBigQuery
    ) -> None:
        """Test InsertDataIntoBigQuery raises GraphError on exception."""
        mock_insert_data_into_bigquery_task.side_effect = Exception("Mocked exception")

        with pytest.raises(GraphError):
            insert_data_into_bigquery(mock_pipeline_state)

        mock_logger.error.assert_called_once_with(
            "Failed to insert data into BigQuery: Mocked exception"
        )
