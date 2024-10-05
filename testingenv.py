from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('api_keys.env')

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Example usage
print(f"OpenAI API Key: {openai_api_key}")
