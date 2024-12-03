import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter
from textwrap import dedent
from src.tasks import check_processed_paper, BigQueryError


class TestCheckProcessedPaper:
    @pytest.fixture
    def mock_client(self) -> Generator[MagicMock, None, None]:
        """Fixture to create a mock BigQuery client."""
        with patch("src.tasks.check_processed_paper.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.project = "test_project"
            yield mock_client

    @pytest.fixture
    def mock_settings(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch `settings`."""
        with patch("src.tasks.check_processed_paper.Settings") as mock_settings:
            mock_settings.return_value.bigquery_dataset_id = "test_dataset"
            yield mock_settings

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch the logger."""
        with patch("src.tasks.check_processed_paper.logger") as mock_logger:
            yield mock_logger

    @pytest.mark.parametrize(
        "paper_id,query_result,expected_result",
        [
            ("paper_1", [{"id": "paper_1"}], True),  # Paper exists
            ("paper_2", [], False),                 # Paper does not exist
        ],
    )
    def test_check_processed_paper(
        self,
        paper_id: str,
        query_result: list,
        expected_result: bool,
        mock_client: MagicMock,
        mock_settings: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test check_processed_paper function with parameterized inputs."""
        mock_client.query.return_value = iter(query_result)

        result = check_processed_paper(paper_id)

        expected_query = dedent(f"""
            SELECT id
            FROM `{mock_client.project}.{mock_settings().bigquery_dataset_id}.research_papers`
            WHERE id = @paper_id
        """).strip()

        expected_job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("paper_id", "STRING", paper_id)
            ]
        )

        # Assert the BigQuery Client is called with the expected query and job config
        mock_client.query.assert_called_once()
        actual_query, actual_kwargs = mock_client.query.call_args
        assert actual_query[0] == expected_query

        assert isinstance(actual_kwargs["job_config"], QueryJobConfig)
        actual_params = actual_kwargs["job_config"].query_parameters
        assert len(actual_params) == len(expected_job_config.query_parameters)
        for actual_param, expected_param in zip(actual_params, expected_job_config.query_parameters):
            assert actual_param.name == expected_param.name
            assert actual_param.type_ == expected_param.type_
            assert actual_param.value == expected_param.value

        # Assert the result is as expected
        assert result == expected_result

        # Verify logging calls
        mock_logger.info.assert_any_call(f"Checking if research paper with ID '{paper_id}' has already been processed")
        mock_logger.info.assert_any_call(f"Research paper with ID '{paper_id}' is{' ' if expected_result else ' not '}processed")

    def test_check_processed_paper_query_error(
        self,
        mock_client: MagicMock,
        mock_settings: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test that an exception is properly raised when the query fails."""
        # Simulate a query error
        mock_client.query.side_effect = Exception("Mocked query error")

        with pytest.raises(BigQueryError, match="Failed to query research paper data: Mocked query error"):
            check_processed_paper("paper_1")

        # Verify logging calls
        mock_logger.info.assert_called_once_with("Checking if research paper with ID 'paper_1' has already been processed")
        mock_logger.error.assert_called_once_with("Failed to query research paper data: Mocked query error")
