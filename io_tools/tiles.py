import subprocess
import os

def selected_attributes_to_list(selected_attributes):
    attributes_list = selected_attributes.split(",")
    return attributes_list

def generate_tiles(args, table, geom_column, shaders_column, output_folder=None, max_features_per_tile=None, attributes=None):
    tiler_path = os.path.join(f"{args.tilers_path}", f"{args.tiler_app}")
    if output_folder is None:
        output_folder = args.output.strip()
    # This part must be removed after md5_implementation would merged on pg2b3dm
    if max_features_per_tile is not None:
        max_features_per_tile = int(max_features_per_tile)*5
    # This part must be removed after md5_implementation would merged on pg2b3dm
    mypass = os.environ.copy()
    mypass['PGPASSWORD']=args.db_password
    # print(args.style_mode)
    attribute_columns = "id,class"

    # Check if the attributes argument specified or not:
    if attributes is not None:
        attribute_columns += ',' + attributes

    if args.tiles_version == "1.0":
        implicit_tiling_option = "false"
    else:
        implicit_tiling_option = "true"

    command = [
        f"{tiler_path}", 
        "--host", f"{args.db_host}", 
        "--username", f"{args.db_username}", 
        "--port", f"{args.db_port}", 
        "--dbname", f"{args.db_name}", 
        "--shaderscolumn", f"{shaders_column}", 
        "--table", f"{table}",
        "--column", f"{geom_column}", 
        "--attributecolumns", f"{attribute_columns}", 
        "--output", f"{output_folder}", 
        "--default_alpha_mode", f"{args.transparency}".upper(), 
        "--max_features_per_tile", f"{max_features_per_tile}",
        "--use_implicit_tiling", f"{implicit_tiling_option}"
    ]
    # print(command)
    # Run the command set above
    sent_command = subprocess.run(
        command, 
        env=mypass,
        capture_output=True, 
        text=True
    )
    # Print out the options as subprocess runs in terminal
    if sent_command.returncode == 0:
        print(sent_command.stdout)
    elif sent_command.returncode != 0:
        print(sent_command.stderr)
    # Information for the user
    print(f"3D Tiles are created based on '{table}' table(materialized view)")
    # Used Command:
    print("Used Command : ", sent_command.stdout)