import pytest
from unittest.mock import Mock, patch
from openai import OpenAI
from src.openai_client import OpenAIClient

class TestOpenAIClient:
    @pytest.fixture(autouse=True)
    def clear_environment(self, monkeypatch):
        """Ensure environment is clean before each test"""
        monkeypatch.delenv('OPENAI_API_KEY', raising=False)
        monkeypatch.delenv('OPENAI_MODEL', raising=False)

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Setup environment variables for testing"""
        monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')
        monkeypatch.setenv('OPENAI_MODEL', 'gpt-4o-mini')

    @pytest.fixture
    def openai_client(self, mock_env_vars):
        """Create OpenAIClient instance with test credentials"""
        return OpenAIClient()

    def test_init_without_api_key(self):
        """Test that OpenAIClient raises error with missing API key"""
        with pytest.raises(ValueError, match="OpenAI API key not found in environment variables"):
            OpenAIClient()

    @patch('src.openai_client.OpenAI')
    def test_send_prompt_success(self, mock_openai_class, mock_env_vars):
        # Setup mock response
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content='{"test": "response"}'))
        ]

        mock_chat = Mock()
        mock_chat.completions.create.return_value = mock_completion

        mock_client = Mock()
        mock_client.chat = mock_chat
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        result = client.send_prompt("Test prompt")

        assert result == {"test": "response"}
        mock_chat.completions.create.assert_called_once_with(
            model=client.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that always responds with valid JSON."},
                {"role": "user", "content": "Test prompt"}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

    @patch('src.openai_client.OpenAI')
    def test_send_prompt_invalid_json(self, mock_openai_class, mock_env_vars):
        # Setup mock response with invalid JSON
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content='Invalid JSON Response'))
        ]

        mock_chat = Mock()
        mock_chat.completions.create.return_value = mock_completion

        mock_client = Mock()
        mock_client.chat = mock_chat
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        with pytest.raises(ValueError) as exc_info:
            client.send_prompt("Test prompt")

        # Verify error message includes the response
        assert "API response was not valid JSON format" in str(exc_info.value)
        assert "Invalid JSON Response" in str(exc_info.value)

    @patch('src.openai_client.OpenAI')
    def test_send_prompt_api_error(self, mock_openai_class, mock_env_vars):
        """Test handling of OpenAI API error"""
        mock_chat = Mock()
        mock_chat.completions.create.side_effect = Exception("API Error")

        mock_client = Mock()
        mock_client.chat = mock_chat
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        with pytest.raises(Exception, match="OpenAI API error: API Error"):
            client.send_prompt("Test prompt")

    @patch('src.openai_client.OpenAI')
    def test_send_prompt_uses_max_tokens(self, mock_openai_class, mock_env_vars):
        """Test that max_tokens is passed to the API call"""
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content='{"test": "response"}'))
        ]

        mock_chat = Mock()
        mock_chat.completions.create.return_value = mock_completion

        mock_client = Mock()
        mock_client.chat = mock_chat
        mock_openai_class.return_value = mock_client

        client = OpenAIClient()
        client.send_prompt("Test prompt")

        call_kwargs = mock_chat.completions.create.call_args[1]
        assert 'max_tokens' in call_kwargs
        assert call_kwargs['max_tokens'] == client.max_tokens

    def test_init_with_custom_max_tokens(self, monkeypatch):
        """Test initialization with custom max tokens"""
        monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')
        monkeypatch.setenv('OPENAI_MAX_TOKENS', '1000')

        client = OpenAIClient()
        assert client.max_tokens == 1000