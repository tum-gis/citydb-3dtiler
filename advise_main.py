#External libraries
import os, sys

# Internal Libraries
from io_tools.pg_sql import read_sql_file
from io_tools.yaml import write_yaml
from database.pg_connection import pg_establish, get_query_results
from classes.advisement2 import Advisement, ObjectClass, ObjectClassRecommendations
from instances.in_advise import *

def advise(args):
    # Establish the Connection with PostgreSQL
    conn = pg_establish(args)

    # Take the existing objectclasses in the database instance
    oc_list, oc_sql_fil = read_sql_file("standalone_queries", "get_all_available_objectclasses.sql")
    result_oc = get_query_results(args, oc_list, name=oc_sql_fil)
    # Take the used command arguments and save as list 
    commandset = dict(args._get_kwargs())

    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            ocs = []
            for oc in result_oc[0]:
                # Set a Where condition for each calculator query that filters objectclasses
                cndtn = f"oc.classname = '{oc}'"
                whrs = WhereElements(
                    WhereElement(condition = cndtn))
                geometry_statistics.where_elements = whrs
                # Calculates Maximum Features per Tile for the specificied Objectclass
                # print(recommended_max_features_per_tile)
                qry_name = "recommended_max_features_per_tile for : " + f"{oc}" + " (instance)"
                oc_statistics = get_query_results(args, str(recommended_max_features_per_tile), name=qry_name)
                rmf = oc_statistics[3] # Statistics Order: 0:min, 1:max, 2:avg, 3:mxm_ftr_pr_tl
                # Add to the list of the ObjectClasses
                oc_new = dict(ObjectClass(oc, objectclass_recommendations = int(rmf)))
                ocs.append(oc_new)
            # Set the Advisement class by considering every objectclasses separately
            adv = Advisement(commandset, max_features=None, objectclasses=ocs)

            try:
                write_yaml("shared", args.output, dict(adv))
            except OSError as err:
                print(f"File Writing Error:\n{err}")
    else:
        # Calculate the recommended max features per tile by considering all the features
        oc_statistics = get_query_results(args, str(recommended_max_features_per_tile), name="recommended_max_features_per_tile (instance)")
        rmf = oc_statistics[3]
        # Add the existing objectclasses to the advisement document
        ocs= []
        for oc in result_oc[0]:
            oc_new = dict(ObjectClass(oc))
            ocs.append(oc_new)
        # Set the advisement class
        adv = Advisement(commandset, max_features=int(rmf), objectclasses = ocs)
        # Write the Advisement as a YAML file
        try:
            write_yaml("shared", args.output, dict(adv))
        except OSError as err:
            print(f"File Writing Error:\n{err}")
