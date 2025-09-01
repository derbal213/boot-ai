import os
from config import *
from google.genai import types
from functions.path_check import check_path

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents for a given file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Read file contents for a given file relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        target_abs = check_path(working_directory, file_path)
        
        with open(target_abs, "r") as file:
            file_content = file.read(MAX_CHARS)
            if os.path.getsize(target_abs) > len(file_content):
                file_content = f'{file_content}\n[...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except OSError as oe:
        return f"    Error: Error running an os action: {oe}"
    except Exception as e:
        return f"    {e}"