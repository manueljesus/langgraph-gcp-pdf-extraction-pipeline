
from google.cloud.bigquery import Client

from src.config import get_settings
from src.utils.hash import generate_unique_hash

class BigQueryError(Exception):
    """Custom exception for errors related to BigQuery interactions."""
    pass

def insert_data_into_bigquery(
    client: Client,
    paper_id: str,
    data: dict
) -> None:
    """
    Insert research paper data into BigQuery tables.

    Args:
        client (Client): BigQuery client.
        paper_id (str): Unique identifier for the research paper.
        data (dict): Research paper data.
    """
    dataset_id: str = get_settings().bigquery_dataset_id

    _insert_research_papers(client, dataset_id, paper_id, data)
    _insert_authors(client, dataset_id, paper_id, data)
    _insert_keywords(client, dataset_id, paper_id, data)
    _insert_key_research_findings(client, dataset_id, paper_id, data)

def _insert_research_papers(
    client: Client,
    dataset_id: str,
    paper_id: str,
    data: dict
) -> None:
    """
    Insert research paper data into research_papers table.

    Args:
        client (Client): BigQuery client.
        dataset_id (str): BigQuery dataset ID.
        paper_id (str): Unique identifier for the research paper.
        data (dict): Research paper data.
    """
    research_paper = [{
        "id": paper_id,
        "title": data["title"],
        "abstract": data["abstract"],
        "summary": data["summary"],
        "methodology": data["methodology"],
        "publication_date": data["publication_date"]
    }]
    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.research_papers", research_paper)
    except Exception as e:
        raise BigQueryError(f"Failed to insert research paper data: {e}")

def _insert_authors(
    client: Client,
    dataset_id: str,
    paper_id: str,
    data: dict
) -> None:
    """
    Insert author data into authors and authors_x_research_papers tables.

    Args:
        client (Client): BigQuery client.
        dataset_id (str): BigQuery dataset ID.
        paper_id (str): Unique identifier for the research paper.
        data (dict): Research paper data.
    """
    authors = list(map(lambda author: {'author_id': generate_unique_hash(author), 'name': author, 'paper_id': paper_id}, data['authors']))

    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.authors", authors, ignore_unknown_values=True, skip_invalid_rows=True)
    except Exception as e:
        raise BigQueryError(f"Failed to insert authors data: {e}")

    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.authors_x_research_papers", authors, ignore_unknown_values=True, skip_invalid_rows=True)
    except Exception as e:
        raise BigQueryError(f"Failed to insert authors_x_research_papers data: {e}")

def _insert_keywords(
    client: Client,
    dataset_id: str,
    paper_id: str,
    data: dict
) -> None:
    """
    Insert keyword data into keywords and keywords_x_research_papers tables.

    Args:
        client (Client): BigQuery client.
        dataset_id (str): BigQuery dataset ID.
        paper_id (str): Unique identifier for the research paper.
        data (dict): Research paper data.
    """
    keywords = list(map(lambda keyword: {'keyword_id': generate_unique_hash(keyword), 'keyword': keyword, 'paper_id': paper_id}, data['keywords']))

    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.keywords", keywords, ignore_unknown_values=True, skip_invalid_rows=True)
    except Exception as e:
        raise BigQueryError(f"Failed to insert keywords data: {e}")

    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.keywords_x_research_papers", keywords, ignore_unknown_values=True, skip_invalid_rows=True)
    except Exception as e:
        raise BigQueryError(f"Failed to insert keywords_x_research_papers data: {e}")

def _insert_key_research_findings(
    client: Client,
    dataset_id: str,
    paper_id: str,
    data: dict
) -> None:
    """
    Insert key research findings data into key_research_findings table.

    Args:
        client (Client): BigQuery client.
        dataset_id (str): BigQuery dataset ID.
        paper_id (str): Unique identifier for the research paper.
        data (dict): Research paper data.
    """
    findings = list(map(lambda finding: {'paper_id': paper_id, 'finding': finding}, data['key_research_findings']))

    try:
        client.insert_rows_json(f"{client.project_id}.{dataset_id}.key_research_findings", findings)
    except Exception as e:
        raise BigQueryError(f"Failed to insert key research findings data: {e}")