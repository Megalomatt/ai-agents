from src.trello_auth import TrelloAuth
from src.agents.project_manager import ProjectManager

def get_first_doing_card(formatted_contents):
    """Extract the first card from the 'Doing' column"""
    doing_list = formatted_contents['lists'].get('Doing', {})
    if not doing_list or not doing_list['cards']:
        raise ValueError("No cards found in 'Doing' column")

    return doing_list['cards'][0]

def main():
    try:
        # Initialize clients
        trello = TrelloAuth()
        project_manager = ProjectManager()

        # Validate Trello credentials
        if trello.validate_credentials():
            print("Successfully authenticated with Trello!")

            # Get and format board contents
            board_contents = trello.get_board_contents()
            formatted_contents = trello.format_board_contents(board_contents)

            # Get the first card from 'Doing' and process it
            current_card = get_first_doing_card(formatted_contents)
            project_manager.process_card(current_card)

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()