import pytest
from typing import Dict, Generator
from unittest.mock import MagicMock, patch
from google.cloud.bigquery import Client
from src.tasks import insert_data_into_bigquery, BigQueryError


class TestInsertDataIntoBigQuery:
    @pytest.fixture
    def mock_client(self) -> Generator[MagicMock, None, None]:
        """Fixture to create a mock BigQuery client."""
        with patch("src.tasks.insert_data_into_bigquery.Client") as mock_client_cls:
            mock_client = MagicMock(spec=Client)
            mock_client_cls.return_value = mock_client
            mock_client.project_id = "test_project"
            yield mock_client

    @pytest.fixture
    def sample_data(self) -> Dict[str, str]:
        """Fixture to provide sample research paper data."""
        return {
            "title": "Sample Paper",
            "abstract": "This is a sample abstract.",
            "summary": "This is a sample summary.",
            "methodology": "This is the methodology section.",
            "publication_date": "2024-01-01",
            "authors": ["Author One", "Author Two"],
            "keywords": ["AI", "Machine Learning"],
            "key_research_findings": ["Finding one", "Finding two"],
        }

    @patch("src.tasks.insert_data_into_bigquery.Settings")
    @patch("src.tasks.insert_data_into_bigquery.generate_unique_hash")
    def test_insert_data_success(
        self,
        mock_generate_hash: MagicMock,
        mock_settings: MagicMock,
        mock_client: MagicMock,
        sample_data: Dict[str, str]
    ):
        """Test successful data insertion into BigQuery."""
        mock_settings.return_value.bigquery_dataset_id = "test_dataset"
        mock_generate_hash.side_effect = lambda x: f"hash_{x}"

        # Call the function
        paper_id = "test_paper_id"
        insert_data_into_bigquery(paper_id, sample_data)

        # Validate that each table insertion method was called with correct arguments
        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.research_papers",
            [{
                "id": paper_id,
                "title": sample_data["title"],
                "abstract": sample_data["abstract"],
                "summary": sample_data["summary"],
                "methodology": sample_data["methodology"],
                "publication_date": sample_data["publication_date"],
            }],
        )

        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.authors",
            [
                {"author_id": "hash_Author One", "name": "Author One", "paper_id": paper_id},
                {"author_id": "hash_Author Two", "name": "Author Two", "paper_id": paper_id},
            ],
            ignore_unknown_values=True,
            skip_invalid_rows=True,
        )

        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.authors_x_research_papers",
            [
                {"author_id": "hash_Author One", "name": "Author One", "paper_id": paper_id},
                {"author_id": "hash_Author Two", "name": "Author Two", "paper_id": paper_id},
            ],
            ignore_unknown_values=True,
            skip_invalid_rows=True,
        )

        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.keywords",
            [
                {"keyword_id": "hash_AI", "keyword": "AI", "paper_id": paper_id},
                {"keyword_id": "hash_Machine Learning", "keyword": "Machine Learning", "paper_id": paper_id},
            ],
            ignore_unknown_values=True,
            skip_invalid_rows=True,
        )

        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.keywords_x_research_papers",
            [
                {"keyword_id": "hash_AI", "keyword": "AI", "paper_id": paper_id},
                {"keyword_id": "hash_Machine Learning", "keyword": "Machine Learning", "paper_id": paper_id},
            ],
            ignore_unknown_values=True,
            skip_invalid_rows=True,
        )

        mock_client.insert_rows_json.assert_any_call(
            "test_project.test_dataset.key_research_findings",
            [
                {"paper_id": paper_id, "finding": "Finding one"},
                {"paper_id": paper_id, "finding": "Finding two"},
            ],
        )

    @patch("src.tasks.insert_data_into_bigquery.Settings")
    def test_insert_data_failure(
        self,
        mock_settings: MagicMock,
        mock_client: MagicMock,
        sample_data: Dict[str, str]
    ):
        """Test BigQueryError is raised on insertion failure."""
        # Mock settings
        mock_settings.return_value.bigquery_dataset_id = "test_dataset"

        # Simulate an insertion failure
        mock_client.insert_rows_json.side_effect = Exception("Mocked insertion error")

        with pytest.raises(BigQueryError, match="Failed to insert research paper data"):
            insert_data_into_bigquery("test_paper_id", sample_data)
