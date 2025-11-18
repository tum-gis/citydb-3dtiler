import os
import shutil

def create_folder(current_path, folder_name):
    new_folder = os.path.join(current_path, folder_name)
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    os.mkdir(new_folder)
    print(f"(i) --> New folder created at {new_folder}")
    return new_folder