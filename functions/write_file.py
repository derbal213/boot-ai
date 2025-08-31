import os

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
