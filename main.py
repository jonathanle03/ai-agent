import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    prompt = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            prompt = arg
    

    if not prompt:
        print("Invalid usage: uv main.py <prompt>")
        sys.exit(1)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )


    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    if "--verbose" in sys.argv:
        print("User prompt: " + prompt)


    print(response.text)


    if "--verbose" in sys.argv:
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))


if __name__ == "__main__":
    main()