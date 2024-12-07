from io import BytesIO
from google.cloud import storage
from src.config import Settings
from src.tasks import GoogleStorageError
from src.logger import get_logger

logger = get_logger(__name__)


def get_file_from_bucket(file_name: str) -> BytesIO:
    """
    Downloads a file from a Google Cloud Storage bucket and returns it as a BytesIO object.

    Args:
        file_name (str): The name of the file to download from the bucket.

    Returns:
        io.BytesIO: An in-memory binary stream containing the file's content.

    Example:
        >>> file_content = get_file_from_bucket("example.txt")
        >>> print(file_content.read().decode('utf-8'))
    """
    try:
        logger.info(f"Downloading file '{file_name}' from Google Cloud Storage")
        # Initialize the Google Cloud Storage client
        storage_client = storage.Client()

        # Retrieve bucket details from settings
        bucket_name = Settings().google_storage_bucket_name
        bucket = storage_client.bucket(bucket_name)

        # Get the blob (file) from the bucket
        blob = bucket.blob(file_name)

        # Download the file as bytes and return it in a BytesIO stream
        file_data = blob.download_as_bytes()
        return BytesIO(file_data)

    except Exception as e:
        logger.error(f"Failed to download file from Google Cloud Storage: {e}")
        raise GoogleStorageError(f"Failed to download file from Google Cloud Storage: {e}")
