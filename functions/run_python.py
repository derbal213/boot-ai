import os
import subprocess
import sys
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file with the given arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run. If not provided, outside the working directory or not a python file, an error will be thrown.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The content to write to the file"
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, file_path))
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.exists(target_abs):
            raise Exception(f'Error: File "{file_path}" not found.')
        
        if not target_abs.endswith(".py"):
            raise Exception(f'Error: "{file_path}" is not a Python file.')
        
        cmd = [sys.executable, target_abs, *args]
        completed = subprocess.run(cmd, timeout=30, capture_output=True, text=True, cwd=wd_abs)

        if completed == None or (completed.stdout.strip() == "" and completed.stderr.strip() == ""):
            return "No output produced"

        stdout = f"STDOUT: {completed.stdout}"
        stderr = f"STDERR: {completed.stderr}"
        results = f"{stdout}\n{stderr}"
        if completed.returncode != 0:
            results = results + "\n" + f"Process exited with code {completed.returncode}"
        return results
    except OSError as oe:
        return f"Error: executing Python file: {oe}"
    except Exception as e:
        return f"Error: executing Python file: {e}" 