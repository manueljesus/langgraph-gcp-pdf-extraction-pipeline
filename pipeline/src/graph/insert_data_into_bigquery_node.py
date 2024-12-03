from typing import Any
from src.graph import PipelineState, GraphError
from src.tasks import insert_data_into_bigquery
from google.cloud.bigquery import Client
from src.logger import get_logger

logger = get_logger(__name__)


class InsertDataIntoBigQuery:
    """
    Pipeline node to insert data into BigQuery
    """
    def __call__(
        self,
        state: PipelineState
    ) -> Any:
        try:
            logger.info(f"Inserting data into BigQuery")
            data = state["state"]
            data.pop("text", None)
            paper_id = data.pop("paper_id")

            insert_data_into_bigquery(
                paper_id,
                data
            )

            return {"state": {}}
        except Exception as e:
            logger.error(f"Failed to insert data into BigQuery: {e}")
            raise GraphError(e)
