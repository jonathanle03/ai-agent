import os


def get_files_info(working_directory, directory="."):
    actual_directory = os.path.abspath(os.path.join(working_directory, directory))
    if not actual_directory.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


    if not os.path.isdir(actual_directory):
        f'Error: "{directory}" is not a directory'
    

    try:
        files = os.listdir(actual_directory)
        contents = ""

        for file in files:
            actual_file = os.path.join(actual_directory, file)
            contents += f" - {os.path.basename(actual_file)}: file_size={os.path.getsize(actual_file)}, is_dir={os.path.isdir(actual_file)}\n"
        
        return contents
    
    except Exception as e:
        return f"Error listing files: {e}"