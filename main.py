from src.trello_auth import TrelloAuth
from src.openai_client import OpenAIClient
import os
import json
from datetime import datetime

# Add this at the top level of the file
temp_dir = 'temp'

def get_first_doing_card(formatted_contents):
    """Extract the first card from the 'Doing' column"""
    doing_list = formatted_contents['lists'].get('Doing', {})
    if not doing_list or not doing_list['cards']:
        raise ValueError("No cards found in 'Doing' column")

    return doing_list['cards'][0]

def generate_user_story_prompt(card):
    """Create a prompt for OpenAI based on the card details"""
    prompt = f"""
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
    return prompt

def print_user_stories(stories_json):
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

def save_user_stories(stories_json):
    """Save the user stories JSON to a temp file"""
    os.makedirs(temp_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'user_stories_{timestamp}.json'
    filepath = os.path.join(temp_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(stories_json, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved user stories to: {filepath}")

def main():
    try:
        # Initialize both clients
        trello = TrelloAuth()
        ai_client = OpenAIClient()

        # Validate Trello credentials
        if trello.validate_credentials():
            print("Successfully authenticated with Trello!")

            # Get and format board contents
            board_contents = trello.get_board_contents()
            formatted_contents = trello.format_board_contents(board_contents)

            # Get the first card from 'Doing'
            current_card = get_first_doing_card(formatted_contents)
            print(f"\nProcessing card: {current_card['name']}")

            # Generate and send prompt to OpenAI
            prompt = generate_user_story_prompt(current_card)
            user_stories = ai_client.send_prompt(prompt, temperature=0.7)

            # Save the JSON response
            save_user_stories(user_stories)

            # Print the results
            print_user_stories(user_stories)

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()