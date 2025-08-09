import os


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