from typing import Union
from io import BytesIO

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from google.cloud.bigquery import Client as BigQueryClient

from src.graph import (
    PipelineState,
    GetFile,
    CheckProcessedPaper,
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
        file: str
    ):
        self.file = file
        self.pipeline: StateGraph = StateGraph(PipelineState)

    def add_nodes(self):
        """
        Add all nodes to the pipeline.
        """
        self.pipeline.add_node("Get File", GetFile(self.file))
        self.pipeline.add_node("Check Processed Paper", CheckProcessedPaper())
        self.pipeline.add_node("Load PDF", LoadPDF())
        self.pipeline.add_node("Extract Metadata", ExtractMetadata())
        self.pipeline.add_node(
            "Extract Key Research Findings And Methodology",
            ExtractKeyResearchFindingsAndMethodology()
        )
        self.pipeline.add_node("Extract Summary And Keywords", ExtractSummaryAndKeywords())
        self.pipeline.add_node("Merge Results", MergeResults())
        self.pipeline.add_node("Insert Data Into BigQuery", InsertDataIntoBigQuery())

    def add_edges(self):
        """
        Add all edges to define the pipeline flow.
        """
        self.pipeline.add_edge(START, "Get File")
        self.pipeline.add_edge("Get File", "Check Processed Paper")
        self.pipeline.add_conditional_edges(
            "Check Processed Paper",
            self._conditional_route,
            {
                "load_pdf": "Load PDF",
                "end": END
            }
        )
        self.pipeline.add_edge("Load PDF", "Extract Metadata")
        self.pipeline.add_edge("Load PDF", "Extract Key Research Findings And Methodology")
        self.pipeline.add_edge("Load PDF", "Extract Summary And Keywords")
        self.pipeline.add_edge("Extract Metadata", "Merge Results")
        self.pipeline.add_edge("Extract Key Research Findings And Methodology", "Merge Results")
        self.pipeline.add_edge("Extract Summary And Keywords", "Merge Results")
        self.pipeline.add_edge("Merge Results", "Insert Data Into BigQuery")
        self.pipeline.add_edge("Insert Data Into BigQuery", END)

    def _conditional_route(self, state: PipelineState) -> str:
        """
        Determine the next node based on the state.
        """
        import pytest
        if state.get('state', {}).get('processed', False):
            return "end"
        return "load_pdf"

    def __call__(self) -> CompiledStateGraph:
        """
        Build and compile the pipeline.
        """
        self.add_nodes()
        self.add_edges()
        self.pipeline = self.pipeline.compile()
        return self.pipeline
