#External Libraries
import sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "./io") # >io_tiles
sys.path.insert(0, "./classes") # >sql_blocks
sys.path.insert(0, "./database") # >pg_connection
sys.path.insert(0, "./instances") # >kernel

# Internal Libraries
from io_tiles import generate_tiles
from sql_blocks import *
from kernel import set_kernel
from pg_connection import create_materialized_view, run_query, index_materialized_view



def tile(args):
    query = set_kernel()
    geom_col = query.select_elements[0].range_alias
    mv_name = "geometries"
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    print(ind_mv)
    run_query(args, crt_mv)
    run_query(args, ind_mv)
    generate_tiles(args, mv_name, f"{geom_col}")



