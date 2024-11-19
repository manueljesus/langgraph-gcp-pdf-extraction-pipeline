import requests

def test_pipeline_e2e() -> None:
    """End-to-end test for the pipeline function."""

    url = "http://localhost:8080"

    # Prepare a CloudEvent payload
    payload = {
        "data": {
            "name": "folder/Test.cs",
            "bucket": "some-bucket",
            "contentType": "application/json",
            "metageneration": "1",
            "timeCreated": "2024-11-19T13:38:57.230Z",
            "updated": "2024-11-19T13:38:57.230Z",
        },
        "type": "google.cloud.storage.object.v1.finalized",
        "specversion": "1.0",
        "source": "//pubsub.googleapis.com/",
        "id": "1234567890",
    }

    headers = {"Content-Type": "application/cloudevents+json"}
    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == 200

    print("Response Content:", response.text)
