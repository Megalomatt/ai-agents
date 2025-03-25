import pytest
import requests
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.trello_auth import TrelloAuth

class TestTrelloAuth:
    @pytest.fixture
    def trello_auth(self, monkeypatch):
        # Mock environment variables for testing
        monkeypatch.setenv('TRELLO_API_KEY', 'test_api_key')
        monkeypatch.setenv('TRELLO_TOKEN', 'test_token')
        monkeypatch.setenv('TRELLO_BOARD_ID', 'test_board_id')
        return TrelloAuth()

    def test_init_with_credentials(self, trello_auth):
        """Test that TrelloAuth initializes with correct credentials"""
        assert trello_auth.api_key == 'test_api_key'
        assert trello_auth.token == 'test_token'
        assert trello_auth.base_url == 'https://api.trello.com/1'

    def test_init_without_credentials(self, monkeypatch):
        """Test that TrelloAuth raises error with missing credentials"""
        monkeypatch.delenv('TRELLO_API_KEY', raising=False)
        monkeypatch.delenv('TRELLO_TOKEN', raising=False)
        monkeypatch.setattr('os.getenv', lambda x, default=None: None)

        trello = TrelloAuth()
        with pytest.raises(ValueError, match="Missing Trello credentials in .env file"):
            trello.validate_credentials()

    def test_validate_credentials_success(self, trello_auth, mocker):
        """Test successful credential validation"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200

        mocker.patch('requests.get', return_value=mock_response)

        assert trello_auth.validate_credentials() is True

    def test_validate_credentials_failure(self, trello_auth, mocker):
        """Test failed credential validation"""
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mocker.patch('requests.get', return_value=mock_response)

        with pytest.raises(requests.exceptions.HTTPError):
            trello_auth.validate_credentials()

    def test_get_board_contents(self, trello_auth, mocker):
        """Test getting board contents"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Test Board',
            'desc': 'Test Description',
            'lists': [],
            'cards': []
        }

        mocker.patch('requests.get', return_value=mock_response)

        board_contents = trello_auth.get_board_contents('test_board_id')
        assert board_contents['name'] == 'Test Board'
        assert board_contents['desc'] == 'Test Description'
        assert 'lists' in board_contents
        assert 'cards' in board_contents

    def test_make_request_with_params(self, trello_auth, mocker):
        """Test making request with additional parameters"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200

        mock_get = mocker.patch('requests.get', return_value=mock_response)

        additional_params = {'fields': 'name,desc'}
        trello_auth.make_request('https://api.trello.com/1/test', additional_params)

        # Verify the request was made with correct parameters
        called_args = mock_get.call_args
        assert called_args[1]['params']['key'] == 'test_api_key'
        assert called_args[1]['params']['token'] == 'test_token'
        assert called_args[1]['params']['fields'] == 'name,desc'

    def test_get_board_contents_no_id(self, trello_auth, mocker):
        """Test getting board contents without providing ID"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Test Board',
            'desc': 'Test Description',
            'lists': [],
            'cards': []
        }

        mocker.patch('requests.get', return_value=mock_response)

        board_contents = trello_auth.get_board_contents()  # No ID provided, uses env
        assert board_contents['name'] == 'Test Board'
        assert board_contents['desc'] == 'Test Description'

    def test_get_board_contents_missing_id(self, monkeypatch, mocker):
        """Test error when no board ID is available"""
        # Mock os.getenv to control exactly what it returns
        def mock_getenv(key, default=None):
            if key == 'TRELLO_API_KEY':
                return 'test_api_key'
            if key == 'TRELLO_TOKEN':
                return 'test_token'
            if key == 'TRELLO_BOARD_ID':
                return None
            return default

        monkeypatch.setattr('os.getenv', mock_getenv)

        # Mock the requests.get to prevent actual HTTP calls
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mocker.patch('requests.get', return_value=mock_response)

        trello = TrelloAuth()

        with pytest.raises(ValueError, match="No board ID provided in .env file or method call"):
            trello.get_board_contents()