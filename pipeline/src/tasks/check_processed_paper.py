from google.cloud.bigquery import Client, QueryJobConfig, ScalarQueryParameter
from textwrap import dedent

from src.config import Settings
from src.tasks import BigQueryError
from src.logger import get_logger

logger = get_logger(__name__)


def check_processed_paper(
    paper_id: str
) -> bool:
    """
    Check if a research paper has already been processed and inserted into BigQuery.

    Args:
        paper_id (str): Unique identifier for the research paper.

    Returns:
        bool: True if the research paper has been processed, False otherwise.
    """
    try:
        logger.info(f"Checking if research paper with ID '{paper_id}' has already been processed")
        client = Client()

        query = dedent(f"""
            SELECT id
            FROM `{client.project}.{Settings().bigquery_dataset_id}.research_papers`
            WHERE id = @paper_id
        """).strip()

        query_job = client.query(
            query,
            job_config=QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("paper_id", "STRING", paper_id)
                ]
            )
        )
        processed = len(list(query_job)) > 0

        logger.info(f"Research paper with ID '{paper_id}' is{' ' if processed else ' not '}processed")

        return processed
    except Exception as e:
        logger.error(f"Failed to query research paper data: {e}")
        raise BigQueryError(f"Failed to query research paper data: {e}")
