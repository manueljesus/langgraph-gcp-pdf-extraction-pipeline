from typing import Union
from io import BytesIO

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from google.cloud.bigquery import Client as BigQueryClient

from src.graph import (
    PipelineState,
    LoadPDF,
    ExtractMetadata,
    ExtractKeyResearchFindingsAndMethodology,
    ExtractSummaryAndKeywords,
    MergeResults,
    InsertDataIntoBigQuery
)


class PipelineBuilder:
    """
    Builder class for the LangGraph pipeline
    """
    def __init__(
        self,
        file: Union[str, BytesIO],
        paper_id: str,
        bigquery_client: BigQueryClient
    ):
        self.file = file
        self.pipeline: StateGraph = StateGraph(PipelineState)
        self.paper_id = paper_id
        self.bigquery_client = bigquery_client

    def add_nodes(self):
        """
        Add all nodes to the pipeline.
        """
        self.pipeline.add_node("Load PDF", LoadPDF(self.file))
        self.pipeline.add_node("Extract Metadata", ExtractMetadata())
        self.pipeline.add_node(
            "Extract Key Research Findings And Methodology",
            ExtractKeyResearchFindingsAndMethodology()
        )
        self.pipeline.add_node("Extract Summary And Keywords", ExtractSummaryAndKeywords())
        self.pipeline.add_node("Merge Results", MergeResults())
        self.pipeline.add_node(
            "Insert Data Into BigQuery",
            InsertDataIntoBigQuery(
                self.bigquery_client,
                self.paper_id
            )
        )

    def add_edges(self):
        """
        Add all edges to define the pipeline flow.
        """
        self.pipeline.add_edge(START, "Load PDF")
        self.pipeline.add_edge("Load PDF", "Extract Metadata")
        self.pipeline.add_edge("Load PDF", "Extract Key Research Findings And Methodology")
        self.pipeline.add_edge("Load PDF", "Extract Summary And Keywords")
        self.pipeline.add_edge("Extract Metadata", "Merge Results")
        self.pipeline.add_edge("Extract Key Research Findings And Methodology", "Merge Results")
        self.pipeline.add_edge("Extract Summary And Keywords", "Merge Results")
        self.pipeline.add_edge("Merge Results", "Insert Data Into BigQuery")
        self.pipeline.add_edge("Insert Data Into BigQuery", END)

    def __call__(self) -> CompiledStateGraph:
        """
        Build and compile the pipeline.
        """
        self.add_nodes()
        self.add_edges()
        self.pipeline = self.pipeline.compile()
        return self.pipeline