# AI Agents Exploration Series

Code and experiments from my YouTube series exploring AI agents and their capabilities. Each branch represents different experiments and implementations shown in the videos.

## Structure
Each branch corresponds to a specific video in the series.

## Videos
[Megalomobile YouTube] (https://www.youtube.com/@megalomatt)

# AI Agents Exploration Series Episode 2

Install required packages:
`pip install python-dotenv requests`

## Trello Setup
1. Get your Trello API credentials:
   - Visit https://trello.com/app-key to get your API key
   - On the same page, click "Generate a Token" to create your token

2. Create a `.env` file in the root directory with your credentials:
   ```
   TRELLO_API_KEY=your_api_key_here
   TRELLO_TOKEN=your_token_here
   ```

3. To use the application, you'll need your board ID:
   - Open your Trello board in a browser
   - The board ID is in the URL: `https://trello.com/b/BOARD_ID/board-name`
   - Copy the BOARD_ID and use it in the main.py file

## Testing
1. Install testing requirements:
   ```
   pip install pytest pytest-mock
   ```

2. Run the tests from the project root directory:
   ```
   # On Windows:
   set PYTHONPATH=src
   pytest tests/

   # On Mac/Linux:
   PYTHONPATH=src pytest tests/
   ```

The tests cover:
- Initialization with and without credentials
- Credential validation
- Board content retrieval
- Request handling with parameters

## License
This is free and unencumbered software released into the public domain. Do whatever you want with it.

This code is experimental and provided as-is, without any warranties or guarantees. You are free to use, modify, and distribute it, but do so at your own discretion.

## Project Structure