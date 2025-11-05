import subprocess
import os

def generate_tiles(args, table, column):
    #print(args)
    tlr = os.path.join(f"{args.tilers_path}", f"{args.tiler_app}")
    output_folder = args.output.strip()
    #print(output_folder)
    mypass = os.environ.copy()
    mypass['PGPASSWORD']=args.db_password
    subprocess.run([f"{tlr}", f"-h {args.db_host}", f"-U {args.db_username}", f"-p {args.db_port}", f"-d {args.db_name}", f"-t {table}", f"-c {column}", f"-a id,class", f"-o{output_folder}"], env=mypass)
    #pg2b3dm -h localhost -U postgres -c geom -d postgres -t sibbe -a identificatie
    print(f"tiles generating based on {table}")