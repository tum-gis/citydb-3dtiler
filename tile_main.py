#External Libraries
import sys
import os

# Internal Libraries
from io_tools.yaml import write_yaml
from io_tools.folder import create_folder
from io_tools.yaml import read_yaml
from io_tools.tiles import generate_tiles
from io_tools.pg_plpgsql import copy_materials
from io_tools.pg_sql import read_sql_file
from database.pg_connection import run_sql
from classes.sql_blocks import *
from instances.kernel import krnl_query
from instances.material import *
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql

def create_tileset(args, output_folder=None, max_features_per_tile=None):
    # Create the materials table on DB
    crt_mat = read_sql_file("advise_sql", "create_materials_for_features_table.sql")
    run_sql(args, crt_mat)
    # Copy the Materials and populate the relevant Views
    copy_materials(args)
    # Populate the relevant tables
    crt_vw_mat_obj = read_sql_file("advise_sql", "vw_material_by_objectclass.sql")
    run_sql(args, crt_vw_mat_obj)
    crt_vw_mat_pro = read_sql_file("advise_sql", "vw_material_by_properties.sql")
    run_sql(args, crt_vw_mat_pro)
    crt_vw_mat_pro_mtchs = read_sql_file("advise_sql", "vw_material_by_properties_matches.sql")
    run_sql(args, crt_vw_mat_pro_mtchs)

    # Set the controller for the materials
    if args.style_mode == 'objectclass-based' and args.style_absence_behavior == 'fall-down':
        krnl_query.select_elements.add(sl_material_by_objectclass_fd)
        krnl_query.join_elements.add(jn_material_by_objectclass)
        #Fall-Down to this Join Element
        krnl_query.join_elements.add(jn_no_material)
    elif args.style_mode == 'custom-attribute-based' and args.style_absence_behavior == 'fall-down':
        krnl_query.join_elements.add(jn_material_by_properties)
        krnl_query.join_elements.add(jn_material_by_objectclass)
        krnl_query.join_elements.add(jn_no_material)

        krnl_query.select_elements.add(sl_material_by_property_fd)
        print(krnl_query)
        
    query = str(krnl_query)
    # Find the geom column in the Select Elements
    for sl in krnl_query.select_elements:
        if sl.range_alias == 'geom':
            geom_col_idx = list(krnl_query.select_elements).index(sl)
    geom_col = str(krnl_query.select_elements[geom_col_idx].range_alias)
    # Finde the shaders column in the Select Elements
    for sl in krnl_query.select_elements:
        if sl.range_alias == 'material_data':
            shaders_col_idx = list(krnl_query.select_elements).index(sl)
    shaders_col = str(krnl_query.select_elements[shaders_col_idx].range_alias)
    
    mv_name = "mv_geometries"
    mfpt = max_features_per_tile
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    run_sql(args, crt_mv)
    run_sql(args, ind_mv)
    generate_tiles(args, mv_name, geom_col, shaders_col, output_folder, mfpt)

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