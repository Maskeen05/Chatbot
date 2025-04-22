import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


# Load the environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Fetch Google API Key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY") # Assuming you have added GOOGLE_API_KEY in .env
print(openai_api_key)
if not openai_api_key:
    raise ValueError("OPENAI API key is missing. Please check the .env file.")

# Now you can proceed with your imports
from chromadb_setup import create_chroma_from_sql

if __name__ == "__main__":
    create_chroma_from_sql()
