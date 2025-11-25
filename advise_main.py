#External libraries
import os, sys

# Internal Libraries
from io_tools.pg_sql import run_sql_file
from io_tools.yaml import write_yaml
from database.pg_connection import pg_establish, get_query_results
# from classes.advisement import Advisement, ObjectClasses, ObjectClass
from classes.advisement2 import Advisement, ObjectClass, ObjectClassProperties
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
    conn = pg_establish(args)

    oc_list = run_sql_file("advise_sql", "get_all_available_objectclasses.sql")
    result_oc = get_query_results(args, oc_list)

    commandset = dict(args._get_kwargs())

    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            ocs = ObjectClasses()
            # ocs = []
            for oc in result_oc[0]:
                cndtn = f"oc.classname = '{oc}'"
                whrs = WhereElements(
                    WhereElement(condition = cndtn))
                addition_of_objectclasses.where_elements = whrs
                oc_statistics = get_query_results(args, str(recommended_max_features_per_tile))
                rmf = oc_statistics[3]
                # ocs = {"name" : oc,
                #     "recommended_max_features" : int(rmf)
                #     }
                # ocs.append(oc_dict)
                ocs.append(ObjectClass(name=oc, recommended_max_features = int(rmf)))
            adv = Advisement(commandset, maxfeature=None, objectclasses=ocs)
            try:
                write_yaml("output", args.output, adv.to_yaml())
            except OSError as err:
                print(f"File Writing Error:\n{err}")
    else:
        oc_statistics = get_query_results(args, str(recommended_max_features_per_tile))
        rmf = oc_statistics[3]
        ocs= []
        # for oc in result_oc[0]:
        #     ocp_new = ObjectClassProperties(max_features = int(rmf))
        #     oc_new = ObjectClass(oc, ocp_new)
        #     ocs.append(oc_new)
        #     # print(ocs)
        for oc in result_oc[0]:
            oc_new = ObjectClass(oc)
            ocs.append(oc_new)
        adv = Advisement(commandset, max_features=int(rmf), objectclasses = ocs)
        print(adv)
        # adv = Advisement(commandset,  maxfeatures=round(rmf))
        # print(adv)
        # try:
        #     write_yaml("output", args.output, adv.to_yaml())
        # except OSError as err:
        #     print(f"File Writing Error:\n{err}")
