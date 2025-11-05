#External Libraries
import sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "./io")
sys.path.insert(0, "./classes")
sys.path.insert(0, "./database/postgresql")
sys.path.insert(0, "./instances")

# Internal Libraries
from tiles_io import generate_tiles
from sql_blocks import *
from kernel import set_kernel
from pg_connection import create_materialized_view, run_query



def tile(args):
    query = set_kernel()
    geom_col = query.select_elements[0].range_alias
    mv_name = "geometries"
    crt_mv = create_materialized_view(mv_name, str(query))
    #print(crt_mv)
    run_query(args, crt_mv)
    generate_tiles(args, mv_name, f"{geom_col}")



