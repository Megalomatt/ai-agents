from openai import OpenAI
import os
import json

class OpenAIClient:
    def __init__(self):
        # Don't use load_dotenv() in init, require explicit key
        self.api_key = os.environ.get('OPENAI_API_KEY')  # Use environ.get directly

        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        self.model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
        self.max_tokens = int(os.environ.get('OPENAI_MAX_TOKENS', '500'))  # Default to 500 tokens

        # Initialize the client with API key
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt, temperature=0.7):
        """
        Send a prompt to OpenAI API and return the JSON response

        Args:
            prompt (str): The prompt to send to the API
            temperature (float): Controls randomness in the response (0.0 to 1.0)

        Returns:
            dict: Parsed JSON response from the API

        Raises:
            ValueError: If the response is not valid JSON
            Exception: For other API errors
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that always responds with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=self.max_tokens,
                response_format={ "type": "json_object" }  # Enforce JSON response
            )

            # Extract the response content
            response_text = response.choices[0].message.content

        except json.JSONDecodeError as e:
            raise ValueError(
                f"API response was not valid JSON format despite requesting JSON.\nReceived response:\n{response_text}"
            )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

        # Move JSON parsing outside the main try-except block
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError(
                f"API response was not valid JSON format.\nReceived response:\n{response_text}"
            )