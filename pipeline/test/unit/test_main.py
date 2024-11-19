from unittest.mock import MagicMock, patch
from cloudevents.http import CloudEvent
import pytest
from src.main import pipeline
from typing import Generator

@pytest.fixture
def mock_cloud_event() -> Generator[CloudEvent, None, None]:
    """Fixture for creating a mock Cloud Storage CloudEvent."""

    attributes = {
        "type": "google.cloud.storage.object.v1.finalized",
        "specversion": "1.0",
        "source": "//pubsub.googleapis.com/",
        "id": "1234567890"
    }

    data = {
        "name": "folder/Test.json",
        "bucket": "some-bucket",
        "contentType": "application/json",
        "metageneration": "1",
        "timeCreated": "2024-11-19T13:38:57.230Z",
        "updated": "2024-11-19T13:38:57.230Z",
    }
    yield CloudEvent(attributes, data)


@patch("logging.info")
def test_pipeline_logs_event(
    mock_logging_info: MagicMock,
    mock_cloud_event: CloudEvent
) -> None:
    """Test the pipeline function logs the CloudEvent correctly."""
    pipeline(mock_cloud_event)

    mock_logging_info.assert_called_once_with(mock_cloud_event)

@patch("logging.exception")
@patch("logging.info")
def test_pipeline_logs_exception(
    mock_logging_info: MagicMock,
    mock_logging_exception: MagicMock,
    mock_cloud_event: CloudEvent
) -> None:
    """Test the pipeline function logs an exception."""

    # Configure mock_logging_info to raise an exception when called
    mock_logging_info.side_effect = Exception("Mocked Exception")

    pipeline(mock_cloud_event)

    mock_logging_exception.assert_called_once()
    args, _ = mock_logging_exception.call_args
    assert "Mocked Exception" in str(args[0])