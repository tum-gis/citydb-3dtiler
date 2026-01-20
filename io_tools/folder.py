import os
import shutil

def create_folder(current_path, folder_name):
    new_folder = os.path.join(current_path, folder_name)
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    os.mkdir(new_folder)
    print(f"(i) --> New folder created at {new_folder}")
    return new_folder

def check_custom_materials(custom_style_file=None):
    materials_folder = os.path.join(os.getcwd(), "shared")
    if custom_style_file == None:
        custom_materials_file = os.path.join(materials_folder, "materials_for_features.csv")
        custom_materials_exists = os.path.exists(custom_materials_file)
    else:
        custom_materials_file = os.path.join(materials_folder, custom_style_file)
        custom_materials_exists = os.path.exists(custom_materials_file)
    custom_materials_dict = {
        exists : custom_materials_exists,
        file_path : custom_materials_file
    }
    return custom_materials_dict

