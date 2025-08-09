import os
import subprocess


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
