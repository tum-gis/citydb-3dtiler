#External Libraries
import sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "./io") # >io_tiles
sys.path.insert(0, "./classes") # >sql_blocks
sys.path.insert(0, "./database") # >pg_connection
sys.path.insert(0, "./instances") # >kernel

# Internal Libraries
from io_tiles import generate_tiles
from io_yaml import read_yaml
from io_folder import create_folder
from sql_blocks import *
from kernel import set_kernel
from pg_connection import create_materialized_view, run_query, index_materialized_view, run_sql

def create_tileset(args, output_folder=None):
    query = set_kernel()
    geom_col = str(query.select_elements[0].range_alias)
    mv_name = "geometries"
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    #print(ind_mv)
    run_sql(args, crt_mv)
    run_sql(args, ind_mv)
    generate_tiles(args, mv_name, geom_col, output_folder)

def tile(args):
    print(args.separate_tilesets)
    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            print("separate tilesets")
            advises = read_yaml(args.output, "advise.yml")
            objectclasses = advises["availableObjectclasses"]
            for oc in objectclasses:
                new_folder = create_folder(args.output, oc)
                #print(new_folder)
                create_tileset(args, output_folder=new_folder)
    else:
        print("ordinary tilesets")
    



