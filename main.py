import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file
from config import *


def main():
    prompt = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            prompt = arg
            break
    
    if not prompt:
        print("Invalid usage: uv main.py <prompt>")
        sys.exit(1)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]


    verbose = "--verbose" in sys.argv
    if verbose:
        print("User prompt: " + prompt)


    counter = 0
    while counter < 20:
        try:    
            response = generate_content(client, messages, available_functions, verbose)
            
            if response.text:
                print(response.text)
                break

            if verbose:
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count

                print("Prompt tokens: " + str(prompt_tokens))
                print("Response tokens: " + str(response_tokens))

            counter += 1
        
        except Exception as e:
            print(f"Error: {e}")


def generate_content(client, messages, available_functions, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )


    for candidate in response.candidates:
        messages.append(candidate.content)


    try:
        function_parts = []
        if response.function_calls:
            for function in response.function_calls:
                result = call_function(function, verbose=verbose)

                if not result.parts or not result.parts[0].function_response:
                    raise Exception("empty function result")
                
                function_parts.append(result.parts[0])

                if verbose:
                    print(f"-> {result.parts[0].function_response}")
            
            messages.append(types.Content(role="tool", parts=function_parts))

    except Exception as e:
        print(f"Error calling function {function.name}({function.args}): {e}")
    
    return response


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")


    function_name = function_call.name
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }


    if not function_name in functions.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    

    function_args = function_call.args.copy()
    function_args["working_directory"] = "./calculator"
    result = functions[function_name](**function_args)


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


if __name__ == "__main__":
    main()