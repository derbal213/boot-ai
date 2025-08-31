import os
from config import *
from google.genai import types

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
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(target_abs):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(target_abs, "r") as file:
            file_content = file.read(MAX_CHARS)
            if os.path.getsize(target_abs) > len(file_content):
                file_content = f'{file_content}\n[...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except OSError as oe:
        return f"    Error: Error running an os action: {oe}"
    except Exception as e:
        return f"    {e}"