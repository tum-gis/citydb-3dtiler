import os
import yaml

# Write YAML file into a specific folder within a specific name
def write_yaml(folder_path, file_name, content):
    file_path = os.path.join(folder_path, file_name)
    try:
        with open(file_path, "w") as advise_file:
            yaml.dump(content, advise_file, width=150, indent=4)
        print(f"(i) File has been created as {file_path}.")
    except OSError as err:
        print(f"(e) File writing error :\n {err}")

def read_yaml(folder_path, file_name):
    relative_file_path = os.path.join(folder_path, file_name)
    try:
        with open(relative_file_path, "r") as advise_file:
            content = yaml.safe_load(advise_file)
    except OSError as err:
        print(f"(e) File reading error :\n {err}")
    return content