import pytest
import json
from unittest.mock import Mock, patch
from src.agents.project_manager import ProjectManager

class TestProjectManager:
    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Setup environment variables for testing"""
        monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')
        monkeypatch.setenv('OPENAI_MODEL', 'gpt-4o-mini')

    @pytest.fixture
    def mock_card(self):
        """Fixture providing a sample card"""
        return {
            'name': 'Test Feature',
            'description': 'Test Description',
            'due': '2024-03-01T12:00:00.000Z',
            'labels': ['Priority']
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

    def test_generate_prompt(self, mock_env_vars, mock_card):
        """Test prompt generation from card details"""
        pm = ProjectManager()
        prompt = pm.generate_prompt(mock_card)
        assert 'Test Feature' in prompt
        assert 'Test Description' in prompt
        assert 'JSON' in prompt
        assert 'epic' in prompt
        assert 'user_stories' in prompt

    def test_save_user_stories(self, mock_env_vars, mock_user_stories, tmp_path):
        """Test saving user stories to temp file"""
        pm = ProjectManager()
        pm.temp_dir = str(tmp_path)

        pm._save_user_stories(mock_user_stories)

        # Check if file was created
        files = list(tmp_path.glob('user_stories_*.json'))
        assert len(files) == 1

        # Verify content
        with open(files[0], 'r', encoding='utf-8') as f:
            saved_content = json.load(f)
            assert saved_content == mock_user_stories

    def test_print_user_stories(self, mock_env_vars, mock_user_stories, capsys):
        """Test user stories printing format"""
        pm = ProjectManager()
        pm._print_user_stories(mock_user_stories)
        captured = capsys.readouterr()

        assert "Epic: Test Epic" in captured.out
        assert "As a user" in captured.out
        assert "I want feature" in captured.out
        assert "So that benefit" in captured.out
        assert "✓ criteria 1" in captured.out

    @patch('src.openai_client.OpenAI')
    def test_process_card(self, mock_openai_class, mock_env_vars, mock_card, mock_user_stories, tmp_path):
        """Test full card processing flow"""
        # Setup mock response
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content=json.dumps(mock_user_stories)))
        ]

        mock_chat = Mock()
        mock_chat.completions.create.return_value = mock_completion

        mock_client = Mock()
        mock_client.chat = mock_chat
        mock_openai_class.return_value = mock_client

        # Process card
        pm = ProjectManager()
        pm.temp_dir = str(tmp_path)
        result = pm.process_card(mock_card)

        # Verify result
        assert result == mock_user_stories

        # Verify file was saved
        files = list(tmp_path.glob('user_stories_*.json'))
        assert len(files) == 1