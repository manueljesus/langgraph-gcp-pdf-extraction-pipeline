import logging

import functions_framework

from cloudevents.http import CloudEvent

logging.basicConfig(level=logging.INFO)

@functions_framework.cloud_event
def pipeline(event: CloudEvent) -> None:
    """Process a cloud event.

    Args:
        event (CloudEvent): CloudEvent object.
    """
    try:
        logging.info(event)
    except Exception as e:
        logging.exception(e)