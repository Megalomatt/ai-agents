from src.trello_auth import TrelloAuth

def print_board_contents(formatted_contents):
    """Print board contents in a readable format"""
    print(f"\nBoard: {formatted_contents['name']}")
    print(f"Description: {formatted_contents['description']}")
    print(f"URL: {formatted_contents['url']}")
    print("\nLists:")

    for list_name, list_contents in formatted_contents['lists'].items():
        print(f"\n  📋 {list_name}")
        if not list_contents['cards']:
            print("    (Empty list)")
        for card in list_contents['cards']:
            print(f"    📌 {card['name']}")
            if card['description']:
                print(f"      Description: {card['description']}")
            if card['due']:
                print(f"      Due: {card['due']}")
            if card['labels']:
                print(f"      Labels: {', '.join(card['labels'])}")

def main():
    try:
        # Initialize Trello authentication
        trello = TrelloAuth()

        # Validate credentials
        if trello.validate_credentials():
            print("Successfully authenticated with Trello!")

            # Get and format board contents
            board_contents = trello.get_board_contents()
            formatted_contents = trello.format_board_contents(board_contents)

            # Print the formatted contents
            print_board_contents(formatted_contents)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()