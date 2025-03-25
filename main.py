from src.trello_auth import TrelloAuth

def main():
    try:
        # Initialize Trello authentication
        trello = TrelloAuth()

        # Validate credentials
        if trello.validate_credentials():
            print("Successfully authenticated with Trello!")

            # Example: Get board contents
            # Replace BOARD_ID with your actual Trello board ID
            board_id = "8LzvPIxy"
            board_contents = trello.get_board_contents(board_id)

            print("\nBoard Information:")
            print(f"Name: {board_contents.get('name')}")
            print(f"Description: {board_contents.get('desc')}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()