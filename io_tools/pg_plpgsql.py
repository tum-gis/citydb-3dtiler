import subprocess
import os

def copy_materials(args):
    mypass = os.environ.copy()
    mypass['PGPASSWORD']=args.db_password
    materials_csv_file_path = os.path.join(os.getcwd(), "materials_for_features", "materials_for_features.csv")
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