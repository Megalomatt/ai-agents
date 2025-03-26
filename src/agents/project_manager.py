import os
import json
from datetime import datetime
from .base_agent import Agent

class ProjectManager(Agent):
    def __init__(self):
        super().__init__()
        self.temp_dir = 'temp'

    def process_card(self, card):
        """Process a card to generate user stories"""
        print(f"\nProcessing card: {card['name']}")

        # Generate and send prompt to OpenAI
        prompt = self.generate_prompt(card)
        user_stories = self.ai_client.send_prompt(prompt, temperature=0.7)

        # Save and print results
        self._save_user_stories(user_stories)
        self._print_user_stories(user_stories)

        return user_stories

    def generate_prompt(self, card):
        """Create a prompt for generating user stories"""
        return f"""
        Generate user stories for the following Trello card task.

        Card Title: {card['name']}
        Description: {card.get('description', 'No description provided')}

        Return a JSON object with this exact structure:
        {{
            "epic": "<The main card title/goal>",
            "user_stories": [
                {{
                    "as_a": "<type of user>",
                    "i_want": "<specific action or feature>",
                    "so_that": "<benefit or value>",
                    "acceptance_criteria": [
                        "<specific requirement 1>",
                        "<specific requirement 2>",
                        "..."
                    ]
                }}
            ]
        }}
        """

    def _save_user_stories(self, stories_json):
        """Save the user stories JSON to a temp file"""
        os.makedirs(self.temp_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'user_stories_{timestamp}.json'
        filepath = os.path.join(self.temp_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stories_json, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Saved user stories to: {filepath}")

    def _print_user_stories(self, stories_json):
        """Print the user stories in a readable format"""
        print("\n📋 Generated User Stories:")
        print(f"\nEpic: {stories_json['epic']}")

        for idx, story in enumerate(stories_json['user_stories'], 1):
            print(f"\n🔹 User Story {idx}:")
            print(f"  As a {story['as_a']}")
            print(f"  I want {story['i_want']}")
            print(f"  So that {story['so_that']}")
            print("\n  Acceptance Criteria:")
            for criteria in story['acceptance_criteria']:
                print(f"  ✓ {criteria}")