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
        """Get the complete contents of a specific board including lists and cards"""
        board_id = board_id or self.board_id
        if not board_id:
            raise ValueError("No board ID provided in .env file or method call")

        url = f"{self.base_url}/boards/{board_id}"
        params = {
            'lists': 'open',
            'cards': 'open',
            'card_fields': 'name,desc,labels,due,idList',
            'fields': 'name,desc,url',
            'list_fields': 'name,pos'
        }
        response = self.make_request(url, params)
        return response.json()

    def get_lists(self, board_id=None):
        """Get all lists (columns) from the board"""
        board_id = board_id or self.board_id
        if not board_id:
            raise ValueError("No board ID provided in .env file or method call")

        url = f"{self.base_url}/boards/{board_id}/lists"
        params = {
            'fields': 'name,pos',
            'cards': 'open'
        }
        response = self.make_request(url, params)
        return response.json()

    def get_cards_in_list(self, list_id):
        """Get all cards from a specific list"""
        if not list_id:
            raise ValueError("List ID is required")

        url = f"{self.base_url}/lists/{list_id}/cards"
        params = {
            'fields': 'name,desc,due,labels'
        }
        response = self.make_request(url, params)
        return response.json()

    def format_board_contents(self, board_contents):
        """Format board contents into a readable structure"""
        formatted = {
            'name': board_contents.get('name'),
            'description': board_contents.get('desc'),
            'url': board_contents.get('url'),
            'lists': {}
        }

        # Group cards by list
        cards_by_list = {}
        for card in board_contents.get('cards', []):
            list_id = card.get('idList')
            if list_id not in cards_by_list:
                cards_by_list[list_id] = []
            cards_by_list[list_id].append(card)

        # Organize lists and their cards
        for lst in board_contents.get('lists', []):
            list_id = lst.get('id')
            formatted['lists'][lst.get('name')] = {
                'cards': [
                    {
                        'name': card.get('name'),
                        'description': card.get('desc'),
                        'due': card.get('due'),
                        'labels': [label.get('name') for label in card.get('labels', [])]
                    }
                    for card in cards_by_list.get(list_id, [])
                ]
            }

        return formatted

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