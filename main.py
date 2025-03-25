from src.trello_auth import TrelloAuth

def main():
    try:
        # Initialize Trello authentication
        trello = TrelloAuth()

        # Validate credentials
        if trello.validate_credentials():
            print("Successfully authenticated with Trello!")

            # Get board contents using ID from environment
            board_contents = trello.get_board_contents()

            print("\nBoard Information:")
            print(f"Name: {board_contents.get('name')}")
            print(f"Description: {board_contents.get('desc')}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()