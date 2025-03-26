import pytest
from unittest.mock import Mock, patch
from main import get_first_doing_card

class TestMain:
    @pytest.fixture
    def mock_formatted_contents(self):
        """Fixture providing sample formatted board contents"""
        return {
            'lists': {
                'To Do': {'cards': []},
                'Doing': {
                    'cards': [
                        {
                            'name': 'Test Card',
                            'description': 'Test Description',
                            'due': '2024-03-01T12:00:00.000Z',
                            'labels': ['Priority']
                        }
                    ]
                },
                'Done': {'cards': []}
            }
        }

    def test_get_first_doing_card(self, mock_formatted_contents):
        """Test extracting first card from Doing column"""
        card = get_first_doing_card(mock_formatted_contents)
        assert card['name'] == 'Test Card'
        assert card['description'] == 'Test Description'

    def test_get_first_doing_card_empty(self):
        """Test handling empty Doing column"""
        empty_contents = {'lists': {'Doing': {'cards': []}}}
        with pytest.raises(ValueError, match="No cards found in 'Doing' column"):
            get_first_doing_card(empty_contents)

    @patch('main.TrelloAuth')
    @patch('main.ProjectManager')
    def test_main_integration(self, mock_pm_class, mock_trello_class, mock_formatted_contents):
        """Test main function integration"""
        # Setup Trello mock
        mock_trello = Mock()
        mock_trello.validate_credentials.return_value = True
        mock_trello.get_board_contents.return_value = {}
        mock_trello.format_board_contents.return_value = mock_formatted_contents
        mock_trello_class.return_value = mock_trello

        # Setup ProjectManager mock
        mock_pm = Mock()
        mock_pm_class.return_value = mock_pm

        # Run main
        from main import main
        main()

        # Verify interactions
        mock_trello.validate_credentials.assert_called_once()
        mock_trello.get_board_contents.assert_called_once()
        mock_pm.process_card.assert_called_once()