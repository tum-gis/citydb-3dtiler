#External libraries
import os, sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "./io")
sys.path.insert(0, "./database/postgresql")
sys.path.insert(0, "./classes")

# Internal Libraries
from yaml_io import write_yaml
from sql_io import read_sql_query
from pg_connection import *
from advisement import Advisement

# Create the advisement dictionary to store the calculations
advisement = {
    "Advises" : {
        "Given Command Arguments" : None,
        "Maximum Feature Number per Tile" : None
        }
}

def advise(args):
    #pg_show_details(args)
    
    conn = pg_establish(args)

    if args.consider_thematic_features == True:
        query = read_sql_query("advise_sql", "calculate_recommended_max_features_per_tile.sql")
    elif args.consider_thematic_features == False:
        query = read_sql_query("advise_sql", "calculate_recommended_max_features_per_tile_only_for_toplevel_features.sql")

    try:
        cur = pg_create_session(conn)
        if pg_check_session(cur):
            cur.execute(query)
        else:
            print("Something went wrong with the database.")
        result = cur.fetchone()
        conn.commit()
        conn.close()
        commandset = dict(args._get_kwargs())
        adv = Advisement(commandset, round(result[3]))
        write_yaml("output", args.output, adv.to_yaml())
    except Error as err:
        print(f"Database error:\n{err}")