#External libraries
import os, sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "./io") # >io_yaml, io_sql
sys.path.insert(0, "./database") # >pg_connection
sys.path.insert(0, "./classes") # >advisement

# Internal Libraries
from io_yaml import write_yaml
from io_sql import read_sql_query
from pg_connection import pg_establish, run_query
from advisement import Advisement
from instances.in_advise import *

# Create the advisement dictionary to store the calculations
advisement = {
    "Advises" : {
        "All Object Classes" : None,
        "Given Command Arguments" : None,
        "Maximum Feature Number per Tile" : None
        }
}

def advise(args):
    #pg_show_details(args)
    
    conn = pg_establish(args)


    oc_list = read_sql_query("advise_sql", "get_all_available_objectclasses.sql")
    result_oc = run_query(args, oc_list)

    #print(result_oc[0])
    commandset = dict(args._get_kwargs())

    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            ocs = []
            for oc in result_oc[0]:
                cndtn = f"oc.classname = '{oc}'"
                whrs = WhereElements(
                    WhereElement(condition = cndtn))
                addition_of_objectclasses.where_elements = whrs
                print(recommended_max_features_per_tile)
                oc_statistics = run_query(args, str(recommended_max_features_per_tile))
                rmf = oc_statistics[3]
                oc_dict = {"name" : oc,
                    "recommended_max_features" : int(rmf)
                    }
                ocs.append(oc_dict)
            # print(ocs)
            adv = Advisement(commandset, maxfeature=None, objectclasses=ocs)
            print(adv.to_yaml())

    # if args.consider_thematic_features == True:
    #     query_max_ftr = read_sql_query("advise_sql", "calculate_recommended_max_features_per_tile.sql")
    # elif args.consider_thematic_features == False:
    #     query_max_ftr = read_sql_query("advise_sql", "calculate_recommended_max_features_per_tile_only_for_toplevel_features.sql")

    

    # result_max_ftr = run_query(args, query_max_ftr)
    
    
    
    
    # adv = Advisement(commandset, round(result_max_ftr[3]), result_oc[0])
    
    try:
        write_yaml("output", args.output, adv.to_yaml())
    except OSError as err:
        print(f"File Writing Error:\n{err}")