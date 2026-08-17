from google import genai
from dotenv import load_dotenv
import os

# .env file se API key load karo
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Client banao
client = genai.Client(api_key=api_key)

# Test question poocho
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Salam! Ek line mein bata do tum kaun ho?"
)

print(response.text)