import pytest
import requests
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.trello_auth import TrelloAuth

class TestTrelloAuth:
    @pytest.fixture
    def mock_board_data(self):
        """Fixture providing sample board data"""
        return {
            'name': 'Test Board',
            'desc': 'Test Description',
            'url': 'https://trello.com/b/test',
            'lists': [
                {
                    'id': 'list1',
                    'name': 'To Do',
                    'pos': 1
                },
                {
                    'id': 'list2',
                    'name': 'Done',
                    'pos': 2
                }
            ],
            'cards': [
                {
                    'id': 'card1',
                    'name': 'Test Card 1',
                    'desc': 'Card Description 1',
                    'due': '2024-03-01T12:00:00.000Z',
                    'idList': 'list1',
                    'labels': [{'name': 'Priority'}]
                },
                {
                    'id': 'card2',
                    'name': 'Test Card 2',
                    'desc': '',
                    'due': None,
                    'idList': 'list2',
                    'labels': []
                }
            ]
        }

    @pytest.fixture
    def trello_auth(self, monkeypatch):
        """Fixture providing TrelloAuth instance with test credentials"""
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

    def test_get_board_contents_with_details(self, trello_auth, mocker, mock_board_data):
        """Test getting detailed board contents"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_board_data

        mocker.patch('requests.get', return_value=mock_response)

        board_contents = trello_auth.get_board_contents()
        assert board_contents['name'] == 'Test Board'
        assert len(board_contents['lists']) == 2
        assert len(board_contents['cards']) == 2

    def test_get_lists(self, trello_auth, mocker):
        """Test getting lists from board"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 'list1', 'name': 'To Do', 'pos': 1},
            {'id': 'list2', 'name': 'Done', 'pos': 2}
        ]

        mocker.patch('requests.get', return_value=mock_response)

        lists = trello_auth.get_lists()
        assert len(lists) == 2
        assert lists[0]['name'] == 'To Do'
        assert lists[1]['name'] == 'Done'

    def test_get_cards_in_list(self, trello_auth, mocker):
        """Test getting cards from a specific list"""
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'name': 'Test Card',
                'desc': 'Description',
                'due': '2024-03-01T12:00:00.000Z',
                'labels': [{'name': 'Priority'}]
            }
        ]

        mocker.patch('requests.get', return_value=mock_response)

        cards = trello_auth.get_cards_in_list('list1')
        assert len(cards) == 1
        assert cards[0]['name'] == 'Test Card'
        assert cards[0]['labels'][0]['name'] == 'Priority'

    def test_get_cards_in_list_no_id(self, trello_auth):
        """Test error when no list ID provided"""
        with pytest.raises(ValueError, match="List ID is required"):
            trello_auth.get_cards_in_list(None)

    def test_format_board_contents(self, trello_auth, mock_board_data):
        """Test formatting board contents"""
        formatted = trello_auth.format_board_contents(mock_board_data)

        assert formatted['name'] == 'Test Board'
        assert formatted['description'] == 'Test Description'
        assert formatted['url'] == 'https://trello.com/b/test'
        assert len(formatted['lists']) == 2

        # Check To Do list
        todo_list = formatted['lists']['To Do']
        assert len(todo_list['cards']) == 1
        assert todo_list['cards'][0]['name'] == 'Test Card 1'
        assert todo_list['cards'][0]['labels'] == ['Priority']

        # Check Done list
        done_list = formatted['lists']['Done']
        assert len(done_list['cards']) == 1
        assert done_list['cards'][0]['name'] == 'Test Card 2'
        assert done_list['cards'][0]['labels'] == []

    def test_format_board_contents_empty(self, trello_auth):
        """Test formatting empty board contents"""
        empty_board = {
            'name': 'Empty Board',
            'desc': '',
            'url': 'https://trello.com/b/empty',
            'lists': [],
            'cards': []
        }

        formatted = trello_auth.format_board_contents(empty_board)
        assert formatted['name'] == 'Empty Board'
        assert formatted['description'] == ''
        assert len(formatted['lists']) == 0