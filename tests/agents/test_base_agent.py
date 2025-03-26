import pytest
from unittest.mock import Mock, patch
from src.agents.base_agent import Agent

class TestAgent:
    class ConcreteAgent(Agent):
        """Concrete implementation for testing abstract base class"""
        def process_card(self, card):
            return self.generate_prompt(card)

        def generate_prompt(self, card):
            return f"Test prompt for {card['name']}"

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Setup environment variables for testing"""
        monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')
        monkeypatch.setenv('OPENAI_MODEL', 'gpt-4o-mini')

    def test_agent_initialization(self, mock_env_vars):
        """Test that agent initializes with OpenAI client"""
        agent = self.ConcreteAgent()
        assert agent.ai_client is not None

    @patch('src.openai_client.OpenAI')
    def test_agent_processes_card(self, mock_openai, mock_env_vars):
        """Test that agent can process a card"""
        agent = self.ConcreteAgent()
        card = {'name': 'Test Card'}
        result = agent.process_card(card)
        assert result == "Test prompt for Test Card"