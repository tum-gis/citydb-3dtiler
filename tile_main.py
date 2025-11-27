#External Libraries
import sys
import os

# Internal Libraries
from io_tools.yaml import write_yaml
from io_tools.folder import create_folder
from io_tools.yaml import read_yaml
from io_tools.tiles import generate_tiles
from classes.sql_blocks import *
from instances.kernel import krnl_query
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql

def create_tileset(args, output_folder=None, max_features_per_tile=None):
    query = str(krnl_query)
    geom_col = str(krnl_query.select_elements[0].range_alias)
    mv_name = "geometries"
    mfpt = max_features_per_tile
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    run_sql(args, crt_mv)
    run_sql(args, ind_mv)
    generate_tiles(args, mv_name, geom_col, output_folder, mfpt)

def tile(args):
    print(args.separate_tilesets)
    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            advises = read_yaml(args.output, "advise.yml")
            objectclasses = advises["objectclasses"]
            # print(objectclasses)
            for oc in objectclasses:
                oc_name = oc["name"]
                oc_mfpt = oc["objectclass_recommendations"]
                new_folder = create_folder(args.output, oc_name)
                oc_folder = os.path.join(args.output, oc_name)
                create_tileset(args, output_folder=oc_folder, max_features_per_tile=oc_mfpt)
    else:
        advises = read_yaml(args.output, "advise.yml")
        create_tileset(args, output_folder=args.output, max_features_per_tile=advises["max_features"])
    



