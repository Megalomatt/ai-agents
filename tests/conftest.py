import os
import sys
import pytest

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Setup environment variables for testing"""
    monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')
    monkeypatch.setenv('OPENAI_MODEL', 'gpt-4o-mini') 