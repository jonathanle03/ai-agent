import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


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


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )


    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )


    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    if "--verbose" in sys.argv:
        print("User prompt: " + prompt)


    for function in response.function_calls:
        print(f"Calling function: {function.name}({function.args})")
    print(response.text)


    if "--verbose" in sys.argv:
        print("Prompt tokens: " + str(prompt_tokens))
        print("Response tokens: " + str(response_tokens))


if __name__ == "__main__":
    main()