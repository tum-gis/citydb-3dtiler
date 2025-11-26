#External Libraries
import sys

# Internal Libraries
from io_tools.yaml import write_yaml
from io_tools.folder import create_folder
from io_tools.yaml import read_yaml
from io_tools.tiles import generate_tiles
from classes.sql_blocks import *
from instances.kernel import krnl_query
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql

def create_tileset(args, output_folder=None):
    query = str(krnl_query)
    geom_col = str(krnl_query.select_elements[0].range_alias)
    mv_name = "geometries"
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
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
                create_tileset(args, output_folder=new_folder)
    else:
        create_tileset(args, output_folder=args.output)
    



