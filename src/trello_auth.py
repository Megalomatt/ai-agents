import os
import requests
from dotenv import load_dotenv

class TrelloAuth:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('TRELLO_API_KEY', None)
        self.token = os.getenv('TRELLO_TOKEN', None)
        self.board_id = os.getenv('TRELLO_BOARD_ID', None)
        self.base_url = "https://api.trello.com/1"

    def validate_credentials(self):
        """Validate that the credentials are working"""
        if not self.api_key or not self.token:
            raise ValueError("Missing Trello credentials in .env file")

        # Let HTTP errors propagate up
        url = f"{self.base_url}/members/me"
        response = self.make_request(url)
        return response.status_code == 200

    def get_board_contents(self, board_id=None):
        """Get the contents of a specific board"""
        # Check for board ID first, before any other operations
        board_id = board_id or self.board_id
        if not board_id:
            raise ValueError("No board ID provided in .env file or method call")

        # Then check credentials
        if not self.api_key or not self.token:
            raise ValueError("Missing Trello credentials in .env file")

        url = f"{self.base_url}/boards/{board_id}"
        params = {
            'lists': 'open',
            'cards': 'open'
        }
        response = self.make_request(url, params)
        return response.json()

    def make_request(self, url, additional_params=None):
        """Make an authenticated request to Trello API"""
        if not self.api_key or not self.token:
            raise ValueError("Missing Trello credentials in .env file")

        params = {
            'key': self.api_key,
            'token': self.token
        }
        if additional_params:
            params.update(additional_params)

        response = requests.get(url, params=params)
        response.raise_for_status()  # This will raise HTTPError for 401
        return response