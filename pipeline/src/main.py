import logging

import functions_framework

from cloudevents.http import CloudEvent
from src.graph import PipelineBuilder

logging.basicConfig(level=logging.INFO)

@functions_framework.cloud_event
def pipeline(event: CloudEvent) -> None:
    """Process a cloud event.

    Args:
        event (CloudEvent): CloudEvent object.
    """
    try:
        logging.info(event)
        pipeline_builder = PipelineBuilder(file=event.data["name"])
        pipeline = pipeline_builder()
        pipeline.invoke({"state": {}})
    except Exception as e:
        logging.exception(e)