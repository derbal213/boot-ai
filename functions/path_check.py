import os

def check_path(working_directory, file_path):
    target_abs = check_path_permitted(working_directory, file_path)
    
    if not os.path.isfile(target_abs):
        raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        
    return target_abs

def check_path_permitted(working_directory, file_path, return_wd=False):
    wd_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    #print(f"------>>>>>  {target_abs}")
    if file_path.startswith(working_directory) and not os.path.exists(target_abs):
        file_path = file_path[len(working_directory) + 1:]
        target_abs = target_abs = os.path.abspath(os.path.join(wd_abs, file_path))

    #print(f"------>>>>>  {target_abs}")
    if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
        raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
    if return_wd:
        return target_abs, wd_abs
    else:
        return target_abs