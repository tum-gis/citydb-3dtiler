import subprocess
import os

def generate_tiles(args, table, column, output_folder=None, max_features_per_tile=None):
    tiler_path = os.path.join(f"{args.tilers_path}", f"{args.tiler_app}")
    if output_folder is None:
        output_folder = args.output.strip()
    mypass = os.environ.copy()
    mypass['PGPASSWORD']=args.db_password
    command = [
        f"{tiler_path}", 
        "--host", f"{args.db_host}", 
        "--username", f"{args.db_username}", 
        "--port", f"{args.db_port}", 
        "--dbname", f"{args.db_name}", 
        "--table", f"{table}",
        "--column", f"{column}", 
        "--attributecolumns", "id,class", 
        "--output", f"{output_folder}", 
        "--max_features_per_tile", f"{max_features_per_tile}"
    ]
    # Run the command set above
    sent_command = subprocess.run(
        command, 
        env=mypass,
        capture_output=True, 
        text=True
    )
    # Print out the options as subprocess runs in terminal
    print(sent_command.stdout)
    # Information for the user
    print(f"3D Tiles are created based on '{table}' table(materialized view)")