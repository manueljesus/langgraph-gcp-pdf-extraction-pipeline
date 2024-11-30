from typing import Any
from src.graph import PipelineState, GraphError
from src.tasks import insert_data_into_bigquery
from google.cloud.bigquery import Client


class InsertDataIntoBigQuery:
    """
    Pipeline node to insert data into BigQuery
    """
    def __init__(
        self,
        client: Client,
        paper_id: str
    ):
        self.client = client
        self.paper_id = paper_id

    def __call__(
        self,
        state: PipelineState
    ) -> Any:
        try:
            data = state["state"]
            data.pop("text", None)

            insert_data_into_bigquery(
                self.client,
                self.paper_id,
                data
            )

            return {"state": {}}
        except Exception as e:
            raise GraphError(e)
