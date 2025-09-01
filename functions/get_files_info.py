import os
from google.genai import types
from functions.path_check import check_path_permitted

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        target_abs = check_path_permitted(working_directory, directory)
        if not os.path.isdir(target_abs):
            raise Exception(f'Error: "{directory}" is not a directory')
        
        files_info = ""
        for file in filter(lambda x : not x.startswith("__"), os.listdir(target_abs)):
            file_path = os.path.join(target_abs, file)
            #print(f"{file} at {file_path}")

            isDir = os.path.isdir(file_path)
            #print(f"{file} is directory = {isDir}")

            file_size = os.path.getsize(file_path)
            #print(f"{file} size = {file_size}")

            file_str = f" - {file}: file_size={file_size} bytes, is_dir={isDir}"
            if files_info == "":
                files_info = file_str
            else:
                files_info = files_info + "\n" + file_str

        return files_info
    except Exception as e:
        #print(error)
        return f"    {e}"