import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from google.auth.exceptions import GoogleAuthError
from typing import Generator
from src.utils.vertex_ai_llama_client import (
    get_credentials,
    get_token,
    get_project_id,
    get_endpoint,
    vertex_ai_llama_request,
    VertexAILlamaError,
)


class TestVertexAILlama:
    """
    Test suite for Vertex AI Llama functions.
    """

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture for patching the logger."""
        with patch("src.utils.vertex_ai_llama_client.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture
    def mock_credentials(self) -> MagicMock:
        """Fixture for mocked Google Cloud credentials."""
        credentials = MagicMock()
        credentials.token = "test_token"
        return credentials

    @pytest.fixture
    def mock_project_id(self) -> str:
        """Fixture for mocked Google Cloud project ID."""
        return "test_project_id"

    @pytest.fixture
    def settings(self) -> MagicMock:
        """Fixture for mocked settings."""
        settings = MagicMock()
        settings.vertex_ai_llama_model = "test_model"
        return settings

    @pytest.fixture
    def patch_google_auth_default(
        self,
        mock_credentials: MagicMock,
        mock_project_id: str
    ) -> Generator[MagicMock, None, None]:
        """Patch src.utils.vertex_ai_llama_client.default to return mock credentials."""
        with patch("src.utils.vertex_ai_llama_client.default") as mock_default:
            mock_default.return_value = (mock_credentials, mock_project_id)
            yield mock_default

    @pytest.fixture
    def patch_get_credentials(
        self,
        mock_credentials: MagicMock,
        mock_project_id: str
    ) -> Generator[MagicMock, None, None]:
        """Patch get_credentials to return mock credentials."""
        with patch("src.utils.vertex_ai_llama_client.get_credentials") as mock_get_credentials:
            mock_get_credentials.return_value = (mock_credentials, mock_project_id)
            yield mock_get_credentials

    @pytest.fixture
    def patch_settings(
        self,
        settings: MagicMock
    ) -> Generator[MagicMock, None, None]:
        """Patch settings to return mock settings."""
        with patch("src.utils.vertex_ai_llama_client.Settings") as mock_settings:
            mock_settings.return_value = settings
            yield mock_settings

    @pytest.fixture
    def patch_requests_post(self) -> Generator[MagicMock, None, None]:
        """Patch requests.post to simulate API responses."""
        with patch("src.utils.vertex_ai_llama_client.requests.post") as mock_post:
            yield mock_post

    def test_get_credentials_success(
        self,
        patch_google_auth_default: MagicMock,
        mock_logger: MagicMock,
        mock_credentials: MagicMock,
        mock_project_id: str
    ):
        """Test get_credentials function with successful retrieval."""
        credentials = get_credentials()
        assert credentials == (mock_credentials, mock_project_id)
        patch_google_auth_default.assert_called_once_with(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        mock_logger.info.assert_called_with("Retrieving Vertex AI credentials")

    def test_get_credentials_refresh_fail(
        self,
        mock_credentials: MagicMock,
        mock_logger: MagicMock
    ):
        """Test get_credentials function with a refresh failure."""
        mock_credentials.refresh.side_effect = GoogleAuthError("Refresh failed")
        with pytest.raises(VertexAILlamaError, match="Failed to get credentials"):
            get_credentials(refresh=True)
        # Verify log calls
        mock_logger.info.assert_called_once_with("Retrieving Vertex AI credentials")
        mock_logger.error.assert_called_with(
            "Failed to get Vertex AI credentials: Your default credentials were not found. "
            "To set up Application Default Credentials, see "
            "https://cloud.google.com/docs/authentication/external/set-up-adc for more information."
        )

    def test_get_token_success(
        self,
        patch_get_credentials: MagicMock,
        mock_logger: MagicMock
    ):
        """Test get_token function with successful token retrieval."""
        token = get_token()
        assert token == "test_token"
        patch_get_credentials.assert_called_once_with(refresh=True)
        mock_logger.info.assert_any_call("Retrieving Vertex AI access token")

    def test_get_project_id_success(
        self,
        patch_get_credentials: MagicMock,
        mock_logger: MagicMock
    ):
        """Test get_project_id function with successful retrieval."""
        project_id = get_project_id()
        assert project_id == "test_project_id"
        patch_get_credentials.assert_called_once_with()
        mock_logger.info.assert_called_with("Retrieving Google Cloud project ID")

    def test_get_endpoint_success(
        self,
        patch_get_credentials: MagicMock,
        mock_logger: MagicMock
    ):
        """Test get_endpoint function with successful URL construction."""
        endpoint = get_endpoint()
        expected_endpoint = (
            "https://us-central1-aiplatform.googleapis.com/v1/projects/test_project_id/locations/us-central1/endpoints/openapi/chat/completions"
        )
        assert endpoint == expected_endpoint
        # Verify both log calls
        mock_logger.info.assert_any_call("Constructing Vertex AI Llama API endpoint")
        mock_logger.info.assert_any_call("Retrieving Google Cloud project ID")

    def test_vertex_ai_llama_request_success(
        self,
        patch_get_credentials: MagicMock,
        patch_settings: MagicMock,
        patch_requests_post: MagicMock,
        mock_logger: MagicMock
    ):
        """Test vertex_ai_llama_request function with successful API call."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test_response"}}]
        }
        patch_requests_post.return_value = mock_response

        response = vertex_ai_llama_request("test_prompt")
        assert response == "test_response"

        mock_logger.info.assert_any_call("Sending request to Vertex AI Llama API")
        mock_logger.info.assert_any_call("Retrieving Vertex AI access token")
