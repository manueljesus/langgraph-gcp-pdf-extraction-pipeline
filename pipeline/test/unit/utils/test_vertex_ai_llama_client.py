import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from google.auth.exceptions import GoogleAuthError
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
    def mock_credentials(self):
        """Fixture for mocked Google Cloud credentials."""
        credentials = MagicMock()
        credentials.token = "test_token"
        credentials.project_id = "test_project_id"
        return credentials

    @pytest.fixture
    def mock_settings(self):
        """Fixture for mocked settings."""
        settings = MagicMock()
        settings.vertex_ai_llama_model = "test_model"
        return settings

    @pytest.fixture
    def patch_google_auth_default(
        self,
        mock_credentials
    ):
        """Patch google.auth.default to return mock credentials."""
        with patch("google.auth.default") as mock_default:
            mock_default.return_value = (mock_credentials, None)
            yield mock_default

    @pytest.fixture
    def patch_get_credentials(
        self,
        mock_credentials
    ):
        """Patch get_credentials to return mock credentials."""
        with patch("src.utils.vertex_ai_llama_client.get_credentials") as mock_get_credentials:
            mock_get_credentials.return_value = mock_credentials
            yield mock_get_credentials

    @pytest.fixture
    def patch_get_settings(
        self,
        mock_settings
    ):
        """Patch get_settings to return mock settings."""
        with patch("src.utils.vertex_ai_llama_client.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock_settings
            yield mock_get_settings

    @pytest.fixture
    def patch_requests_post(self):
        """Patch requests.post to simulate API responses."""
        with patch("src.utils.vertex_ai_llama_client.requests.post") as mock_post:
            yield mock_post

    def test_get_credentials_success(
        self,
        mock_credentials
    ):
        """
        Test get_credentials function with successful retrieval by patching the default function.
        """
        with patch("src.utils.vertex_ai_llama_client.default", return_value=(mock_credentials, None)) as mock_default:
            credentials = get_credentials()
            assert credentials == mock_credentials
            mock_default.assert_called_once_with(scopes=["https://www.googleapis.com/auth/cloud-platform"])

    def test_get_credentials_refresh_fail(
        self,
        patch_google_auth_default,
        mock_credentials
    ):
        """
        Test get_credentials function with a refresh failure.
        """
        mock_credentials.refresh.side_effect = GoogleAuthError("Refresh failed")
        with pytest.raises(VertexAILlamaError, match="Failed to get credentials"):
            get_credentials(refresh=True)

    def test_get_token_success(
        self,
        patch_get_credentials
    ):
        """
        Test get_token function with successful token retrieval.
        """
        token = get_token()
        assert token == "test_token"
        patch_get_credentials.assert_called_once_with(refresh=True)

    def test_get_token_failure(
        self,
        patch_get_credentials
    ):
        """
        Test get_token function with failure in token retrieval.
        """
        patch_get_credentials.side_effect = VertexAILlamaError("Credential failure")
        with pytest.raises(VertexAILlamaError, match="Failed to get access token"):
            get_token()

    def test_get_project_id_success(
        self,
        patch_get_credentials
    ):
        """
        Test get_project_id function with successful retrieval.
        """
        project_id = get_project_id()
        assert project_id == "test_project_id"
        patch_get_credentials.assert_called_once_with()

    def test_get_project_id_failure(
        self,
        patch_get_credentials
    ):
        """
        Test get_project_id function with failure in retrieval.
        """
        patch_get_credentials.side_effect = VertexAILlamaError("Project ID failure")
        with pytest.raises(VertexAILlamaError, match="Failed to get project ID"):
            get_project_id()

    def test_get_endpoint_success(
        self,
        patch_get_credentials
    ):
        """
        Test get_endpoint function with successful URL construction.
        """
        endpoint = get_endpoint()
        expected_endpoint = (
            "https://us-central1-aiplatform.googleapis.com/v1/projects/test_project_id/locations/us-central1/endpoints/openapi/chat/completions"
        )
        assert endpoint == expected_endpoint

    def test_get_endpoint_failure(self, patch_get_credentials):
        """
        Test get_endpoint function with failure in project ID retrieval.
        """
        patch_get_credentials.side_effect = VertexAILlamaError("Project ID failure")
        with pytest.raises(VertexAILlamaError, match="Failed to construct API endpoint"):
            get_endpoint()

    def test_vertex_ai_llama_request_success(
        self,
        patch_get_credentials,
        patch_get_settings,
        patch_requests_post
    ):
        """
        Test vertex_ai_llama_request function with successful API call.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test_response"}}]
        }
        patch_requests_post.return_value = mock_response

        response = vertex_ai_llama_request("test_prompt")
        assert response == "test_response"

        patch_requests_post.assert_called_once_with(
            "https://us-central1-aiplatform.googleapis.com/v1/projects/test_project_id/locations/us-central1/endpoints/openapi/chat/completions",
            headers={
                "Authorization": f"Bearer test_token",
                "Content-Type": "application/json",
            },
            json={
                "model": "test_model",
                "stream": False,
                "messages": [{"role": "user", "content": "test_prompt"}],
            },
            timeout=30,
        )

    def test_vertex_ai_llama_request_failure(
        self,
        patch_get_credentials,
        patch_get_settings,
        patch_requests_post
    ):
        """
        Test vertex_ai_llama_request function with an HTTP failure.
        """
        patch_requests_post.side_effect = RequestException("HTTP error")
        with pytest.raises(VertexAILlamaError, match="HTTP request failed"):
            vertex_ai_llama_request("test_prompt")
