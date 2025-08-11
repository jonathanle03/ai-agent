import os
from google.genai import types


def write_file(working_directory, file_path, content):
    actual_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not actual_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    

    try:
        if not os.path.exists(actual_file_path):
            f = open(actual_file_path, "x")
            f.close()
        
        with open(actual_file_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error writing to file: {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the file.",
            ),
        },
    ),
)