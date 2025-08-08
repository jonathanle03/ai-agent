import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) == 1:
    print("Invalid usage: uv main.py <prompt>")
    sys.exit(1)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]


response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages
)


print(response.text)
print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
print("Response tokens: " + str(response.usage_metadata.candidates_token_count))
