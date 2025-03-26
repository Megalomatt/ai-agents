import pytest
import json
import os
from unittest.mock import Mock, patch
from datetime import datetime

# Import the functions from main
from main import (
    get_first_doing_card,
    generate_user_story_prompt,
    save_user_stories,
    print_user_stories
)

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

    @pytest.fixture
    def mock_user_stories(self):
        """Fixture providing sample user stories JSON"""
        return {
            "epic": "Test Epic",
            "user_stories": [
                {
                    "as_a": "user",
                    "i_want": "feature",
                    "so_that": "benefit",
                    "acceptance_criteria": ["criteria 1", "criteria 2"]
                }
            ]
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

    def test_generate_user_story_prompt(self):
        """Test prompt generation from card details"""
        card = {
            'name': 'Test Feature',
            'description': 'Test Description'
        }
        prompt = generate_user_story_prompt(card)
        assert 'Test Feature' in prompt
        assert 'Test Description' in prompt
        assert 'JSON' in prompt

    def test_save_user_stories(self, mock_user_stories, tmp_path):
        """Test saving user stories to temp file"""
        # Use pytest tmp_path fixture for temporary directory
        with patch('main.temp_dir', str(tmp_path)):
            save_user_stories(mock_user_stories)

            # Check if file was created
            files = list(tmp_path.glob('user_stories_*.json'))
            assert len(files) == 1

            # Verify content
            with open(files[0], 'r', encoding='utf-8') as f:
                saved_content = json.load(f)
                assert saved_content == mock_user_stories

    def test_print_user_stories(self, mock_user_stories, capsys):
        """Test user stories printing format"""
        print_user_stories(mock_user_stories)
        captured = capsys.readouterr()

        assert "Epic: Test Epic" in captured.out
        assert "As a user" in captured.out
        assert "I want feature" in captured.out
        assert "So that benefit" in captured.out
        assert "✓ criteria 1" in captured.out

    @patch('main.TrelloAuth')
    @patch('main.OpenAIClient')
    def test_main_integration(self, mock_openai, mock_trello, mock_formatted_contents, mock_user_stories, tmp_path):
        """Test main function integration"""
        # Setup mocks
        mock_trello_instance = Mock()
        mock_trello_instance.validate_credentials.return_value = True
        mock_trello_instance.get_board_contents.return_value = {}
        mock_trello_instance.format_board_contents.return_value = mock_formatted_contents
        mock_trello.return_value = mock_trello_instance

        mock_openai_instance = Mock()
        mock_openai_instance.send_prompt.return_value = mock_user_stories
        mock_openai.return_value = mock_openai_instance

        # Run main with temporary directory
        with patch('main.temp_dir', str(tmp_path)):
            from main import main
            main()

        # Verify interactions
        mock_trello_instance.validate_credentials.assert_called_once()
        mock_trello_instance.get_board_contents.assert_called_once()
        mock_openai_instance.send_prompt.assert_called_once()