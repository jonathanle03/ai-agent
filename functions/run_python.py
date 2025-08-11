import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    actual_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not actual_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    

    if not os.path.isfile(actual_file_path):
        return f'Error: File "{file_path}" not found.'


    if not actual_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        arguments = ["uv", "run", file_path]
        arguments.extend(args)
        result = subprocess.run(cwd=os.path.abspath(working_directory), args=arguments, timeout=30, capture_output=True)

        if result == None:
            return "No output produced"
        
        output = f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
        if result.returncode != 0:
            output += f", Process exited with code {result.returncode}"
        
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python function in the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that contains the function to be ran, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.OBJECT,
                description="The arguments that are used for the function call.",
            ),
        },
    ),
)