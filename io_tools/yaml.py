import os
import yaml

# Write YAML file into a specific folder within a specific name
def write_yaml(folder, file_name, content):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path, "w") as advise_file:
            yaml.safe_dump(content, advise_file, width=150, indent=4)
        print(f"(i)--> File has been created as {relative_file_path}.")
    except OSError as err:
        print(f"(e)--> File writing error :\n {err}")

def read_yaml(folder, file_name):
    relative_file_path = os.path.join(folder, file_name)
    try:
        with open(relative_file_path, "r") as advise_file:
            content = yaml.safe_load(advise_file)
    except OSError as err:
        print(f"(e)--> File reading error :\n {err}")
    return content