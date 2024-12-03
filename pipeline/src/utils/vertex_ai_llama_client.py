import requests
from google.auth import default
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from src.config import Settings
from src.logger import get_logger

logger = get_logger(__name__)


class VertexAILlamaError(Exception):
    """Custom exception for errors related to Vertex AI Llama interactions."""
    pass


def get_credentials(refresh: bool = False):
    """
    Retrieve Google Cloud credentials.

    Args:
        refresh (bool): Whether to refresh the credentials before returning.

    Returns:
        google.auth.credentials.Credentials: The authenticated credentials.
        str: The Google Cloud project ID.

    Raises:
        VertexAILlamaError: If credentials retrieval or refresh fails.
    """
    try:
        logger.info("Retrieving Vertex AI credentials")
        credentials, project_id = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])

        if refresh:
            logger.info("Refreshing Vertex AI credentials")
            credentials.refresh(Request())

        return credentials, project_id
    except GoogleAuthError as e:
        logger.error(f"Failed to get Vertex AI credentials: {e}")
        raise VertexAILlamaError(f"Failed to get credentials: {e}")


def get_token():
    """
    Retrieve an OAuth 2.0 token for API requests.

    Returns:
        str: The access token.

    Raises:
        VertexAILlamaError: If token retrieval fails.
    """
    try:
        logger.info("Retrieving Vertex AI access token")
        credentials, _ = get_credentials(refresh=True)
        return credentials.token
    except VertexAILlamaError as e:
        logger.error(f"Failed to get Vertex AI access token: {e}")
        raise VertexAILlamaError(f"Failed to get access token: {e}")


def get_project_id():
    """
    Retrieve the project ID from the default credentials.

    Returns:
        str: The Google Cloud project ID.

    Raises:
        VertexAILlamaError: If project ID retrieval fails.
    """
    try:
        logger.info("Retrieving Google Cloud project ID")
        _, project_id = get_credentials()
        return project_id
    except VertexAILlamaError as e:
        logger.error(f"Failed to get Google Cloud project ID: {e}")
        raise VertexAILlamaError(f"Failed to get project ID: {e}")


def get_endpoint():
    """
    Construct the Vertex AI Llama API endpoint URL.

    Returns:
        str: The full API endpoint URL.

    Raises:
        VertexAILlamaError: If project ID retrieval fails.
    """
    try:
        logger.info("Constructing Vertex AI Llama API endpoint")
        project_id = get_project_id()
        return f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/endpoints/openapi/chat/completions"
    except VertexAILlamaError as e:
        logger.error(f"Failed to construct API endpoint: {e}")
        raise VertexAILlamaError(f"Failed to construct API endpoint: {e}")


def vertex_ai_llama_request(prompt: str) -> str:
    """
    Send a request to the Vertex AI Llama API service.

    Args:
        prompt (str): The user input prompt for the Llama model.

    Returns:
        str: The model's response to the prompt.

    Raises:
        VertexAILlamaError: If the API request or response processing fails.
    """
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": Settings().vertex_ai_llama_model,
        "stream": False,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        logger.info("Sending request to Vertex AI Llama API")
        response = requests.post(
            get_endpoint(),
            headers=headers,
            json=payload,
            timeout=30  # Add a timeout for better reliability
        )
        response.raise_for_status()
        choices = response.json().get('choices', [])
        if not choices:
            logger.error("No choices returned in the response.")
            raise VertexAILlamaError("No choices returned in the response.")
        return choices[-1].get('message', {}).get('content', '')
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e}")
        raise VertexAILlamaError(f"HTTP request failed: {e}")
    except KeyError:
        logger.error("Unexpected response format.")
        raise VertexAILlamaError("Unexpected response format.")
    except Exception as e:
        logger.error(f"An error occurred while sending the request: {e}")
        raise VertexAILlamaError(f"An error occurred while sending the request: {e}")
