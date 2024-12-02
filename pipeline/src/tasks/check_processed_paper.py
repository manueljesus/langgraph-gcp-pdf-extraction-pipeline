from google.cloud.bigquery import Client, QueryJobConfig, ScalarQueryParameter
from textwrap import dedent

from src.config import get_settings
from src.tasks import BigQueryError

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
        client = Client()

        query = dedent(f"""
            SELECT id
            FROM `@project_id.@dataset_id.research_papers`
            WHERE id = @paper_id
        """).strip()

        query_job = client.query(
            query,
            job_config=QueryJobConfig(
                query_parameters=[
                    ScalarQueryParameter("project_id", "STRING", client.project),
                    ScalarQueryParameter("dataset_id", "STRING", get_settings().bigquery_dataset_id),
                    ScalarQueryParameter("paper_id", "STRING", paper_id)
                ]
            )
        )

        return len(list(query_job)) > 0
    except Exception as e:
        raise BigQueryError(f"Failed to query research paper data: {e}")
