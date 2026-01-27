import subprocess
import os

mypass = os.environ.copy()

def copy_materials(args, custom_materials=None):
    mypass['PGPASSWORD']=args.db_password
    if custom_materials == None:
        materials_csv_file_path = os.path.join(os.getcwd(), "materials_for_features", "materials_for_features.csv")
    else:
        materials_csv_file_path = os.path.join(os.getcwd(), "shared", custom_materials)
    # print(materials_csv_file_path)
    # print(args)
    command = [
        "psql", 
        "--host", f"{args.db_host}", 
        "--username", f"{args.db_username}", 
        "--port", f"{args.db_port}", 
        "--dbname", f"{args.db_name}", 
        "--command", f"\\COPY _materials_for_features (namespace_of_classname,classname,namespace_of_property,property_name,column_name_of_property_value,property_value,emmisive_color,pbr_metallic_roughness_base_color,pbr_metallic_roughness_metallic_roughness,pbr_specular_glossiness_diffuse_color,pbr_specular_glossiness_specular_glossiness) FROM '{materials_csv_file_path}' DELIMITER ',' CSV HEADER;", 
        "--variable", "ON_ERROR_STOP=1"
    ]
    sent_command = subprocess.run(
        command, 
        env=mypass,
        capture_output=True, 
        text=True
        )
    if sent_command.returncode == 0:
        print(sent_command.stdout)
    else:
        print(sent_command.stderr)

def drop_cascade_if_exists(args, table_name):
    mypass['PGPASSWORD']=args.db_password
    command = [
        "psql", 
        "--host", f"{args.db_host}", 
        "--username", f"{args.db_username}", 
        "--port", f"{args.db_port}", 
        "--dbname", f"{args.db_name}", 
        "--command", f"DROP TABLE IF EXISTS {table_name} CASCADE;", 
        "--variable", "ON_ERROR_STOP=1"
    ]
    sent_command = subprocess.run(
        command, 
        env=mypass,
        capture_output=True, 
        text=True
        )
    if sent_command.returncode == 0:
        print(f"Following table has been dropped within cascade method : {table_name}.")
        print(sent_command.stdout)
    else:
        print(sent_command.stderr)