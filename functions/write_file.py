import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates and writes the given content to a given file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Creates and writes the given content to a given file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file"
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))
        print(target_abs)
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.exists(target_abs):
            os.makedirs(os.path.dirname(target_abs), exist_ok=True)

        with open(target_abs, "w") as f:
            f.write(content)
    
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as oe:
        return f"    Error: Error running an os action: {oe}"
    except Exception as e:
        return f"    {e}"
