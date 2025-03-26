from abc import ABC, abstractmethod
from src.openai_client import OpenAIClient

class Agent(ABC):
    """Base class for all agents"""
    def __init__(self):
        self.ai_client = OpenAIClient()

    @abstractmethod
    def process_card(self, card):
        """Process a Trello card according to the agent's specialty"""
        pass

    @abstractmethod
    def generate_prompt(self, card):
        """Generate a prompt specific to the agent's purpose"""
        pass