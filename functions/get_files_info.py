import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, directory))
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        if not os.path.isdir(target_abs):
            raise Exception(f'Error: "{directory}" is not a directory')
        
        files_info = ""
        for file in filter(lambda x : not x.startswith("__") and not x.endswith(".txt"), os.listdir(full_path)):
            file_path = os.path.join(full_path, file)
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