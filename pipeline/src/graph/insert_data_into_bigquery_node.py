from typing import Any
from src.graph import PipelineState, GraphError
from src.tasks import insert_data_into_bigquery
from google.cloud.bigquery import Client


class InsertDataIntoBigQuery:
    """
    Pipeline node to insert data into BigQuery
    """
    def __call__(
        self,
        state: PipelineState
    ) -> Any:
        try:
            data = state["state"]
            data.pop("text", None)
            paper_id = data.pop("paper_id")

            insert_data_into_bigquery(
                paper_id,
                data
            )

            return {"state": {}}
        except Exception as e:
            raise GraphError(e)
