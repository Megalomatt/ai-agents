# AI Agents Exploration Series

Code and experiments from my YouTube series exploring AI agents and their capabilities. Each branch represents different experiments and implementations shown in the videos.

## Structure
Each branch corresponds to a specific video in the series.

## Videos
[My AI Dev Team Part 1 - Agents](https://www.youtube.com/watch?v=WiNIFcBo0vs)
[I Made My To-Do List Read Itself - Here's How](https://youtu.be/LOzST1WEJMc)
[Can AI Run Your Project Better Than You?](https://youtu.be/VfmZZz9iRx8)

# AI Agents Exploration Series Episode 3
## Can AI Run Your Project Better Than You?

Install required packages:
```bash
pip install python-dotenv requests openai
```

## Trello Setup
1. Get your Trello API credentials:
   - Visit https://trello.com/app-key to get your API key
   - On the same page, click "Generate a Token" to create your token

2. Copy the `.example.env` file to create a new `.env` file:
   ```
   cp .example.env .env
   ```

3. Fill in your credentials in the `.env` file:
   ```
   TRELLO_API_KEY=your_api_key_here
   TRELLO_TOKEN=your_token_here
   TRELLO_BOARD_ID=your_board_id_here
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini  # or gpt-4, or any other available model
   ```

4. To get your board ID:
   - Open your Trello board in a browser
   - The board ID is in the URL: `https://trello.com/b/BOARD_ID/board-name`

## Testing
1. Install testing requirements:
   ```
   pip install pytest pytest-mock
   ```

2. Run the tests from the project root directory:
   ```
   pytest
   ```

The tests cover:
- TrelloAuth initialization and credential handling
- API credential validation
- Board content retrieval and formatting
- List and card operations
- Error handling for missing credentials/IDs
- Request parameter handling
- Response formatting and data structure validation

Each test case ensures proper functionality of the Trello integration, including:
- Handling of environment variables
- API request formatting
- Response parsing
- Error conditions
- Data transformation and formatting

## License
This is free and unencumbered software released into the public domain. Do whatever you want with it.

This code is experimental and provided as-is, without any warranties or guarantees. You are free to use, modify, and distribute it, but do so at your own discretion.
