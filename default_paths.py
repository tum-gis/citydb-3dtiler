#External libraries
import os

def get_base_path():
  base_path = os.getcwd()
  return base_path

def get_shared_folder_path():
  shared_folder_path = os.path.join(os.getcwd(), "shared")
  return shared_folder_path