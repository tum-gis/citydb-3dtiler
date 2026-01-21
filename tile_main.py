#External Libraries
import sys
import os

# Internal Libraries
from io_tools.yaml import write_yaml
from io_tools.folder import create_folder, check_custom_materials
from io_tools.yaml import read_yaml
from io_tools.tiles import generate_tiles
from io_tools.pg_plpgsql import copy_materials
from io_tools.pg_sql import read_sql_file
from database.pg_connection import run_sql
from classes.sql_blocks import *
from instances.kernel import krnl_query
from instances.material import objectclass_falldown_query, custom_property_falldown_query
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql

def create_tileset(args, output_folder=None, max_features_per_tile=None, whrs=None):
    # Create the materials table on DB
    crt_mat, crt_mat_fl_nm = read_sql_file("standalone_queries", "create_materials_for_features_table.sql")
    run_sql(args, crt_mat, name=crt_mat_fl_nm)
    
    # Check for Custom Materials and copy the Materials and populate the relevant Views
    # Check if the user specified a custom style other than "materials_for_features"
    if args.custom_style == "materials_for_features.csv":
        custom_material = check_custom_materials()
    else:
        custom_material = check_custom_materials(args.custom_style)
    # If the custom_material exists in the shared folder,
    #  then consider this file,
    #  otherwise use the default materials_for_features file in repository.
    if custom_material["exists"] == True:
        copy_materials(args, custom_material["file_path"])
    else:
        copy_materials(args)

    # Populate the relevant tables
    crt_vw_mat_obj, crt_vw_mat_obj_fl_nm = read_sql_file("standalone_queries", "vw_material_by_objectclass.sql")
    run_sql(args, crt_vw_mat_obj, name=crt_vw_mat_obj_fl_nm)
    crt_vw_mat_pro, crt_vw_mat_pro_fl_nm = read_sql_file("standalone_queries", "vw_material_by_properties.sql")
    run_sql(args, crt_vw_mat_pro, name= crt_vw_mat_pro_fl_nm)
    crt_vw_mat_pro_mtchs, crt_vw_mat_pro_mtchs_fl_nm = read_sql_file("standalone_queries", "vw_material_by_properties_matches.sql")
    run_sql(args, crt_vw_mat_pro_mtchs, name=crt_vw_mat_pro_mtchs_fl_nm)

    # Set the controller for the materials
    if args.style_mode == 'objectclass-based' and args.style_absence_behavior == 'fall-down':
        
        # If any filter is given, add the filter to the query
        if whrs != None:
            objectclass_falldown_query[0].where_elements = whrs
        query = str(objectclass_falldown_query)

        # Find the geom column in the Select Elements
        for sl in objectclass_falldown_query.select_elements:
            if sl.range_alias == 'geom':
                geom_col_idx = list(objectclass_falldown_query.select_elements).index(sl)
        geom_col = str(objectclass_falldown_query.select_elements[geom_col_idx].range_alias)

        # Find the shaders column in the Select Elements
        for sl in objectclass_falldown_query.select_elements:
            if sl.range_alias == 'material_data':
                shaders_col_idx = list(objectclass_falldown_query.select_elements).index(sl)
        shaders_col = str(objectclass_falldown_query.select_elements[shaders_col_idx].range_alias)
        
    elif args.style_mode == 'property-based' and args.style_absence_behavior == 'fall-down':
        
        # If any filter is given, add the filter to the query
        if whrs != None:
            custom_property_falldown_query[0].where_elements = whrs
        query = str(custom_property_falldown_query)
        
        # Find the geom column in the Select Elements
        for sl in custom_property_falldown_query.select_elements:
            if sl.range_alias == 'geom':
                geom_col_idx = list(custom_property_falldown_query.select_elements).index(sl)
        geom_col = str(custom_property_falldown_query.select_elements[geom_col_idx].range_alias)
        
        # Find the shaders column in the Select Elements
        for sl in custom_property_falldown_query.select_elements:
            if sl.range_alias == 'material_data':
                shaders_col_idx = list(custom_property_falldown_query.select_elements).index(sl)
        shaders_col = str(custom_property_falldown_query.select_elements[shaders_col_idx].range_alias)

    # Set the name of materialized view that would be used for tiling
    mv_name = "mv_geometries"
    mfpt = max_features_per_tile
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    # print(crt_mv)
    run_sql(args, crt_mv, name=f"create_materialized_view (function) for {mv_name}")
    run_sql(args, ind_mv, name=f"index_materialized_view (function) for {mv_name}")
    generate_tiles(args, mv_name, geom_col, shaders_col, output_folder, mfpt)

def tile(args):
    print(args.separate_tilesets)
    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            advises = read_yaml(args.output, "advise.yml")
            objectclasses = advises["objectclasses"]
            
            for oc in objectclasses:
                oc_name = oc["name"]
                oc_mfpt = oc["objectclass_recommendations"]
                new_folder = create_folder(args.output, oc_name)
                oc_folder = os.path.join(args.output, oc_name)
                
                # Set a Where condition for each calculator query that filters objectclasses
                cndtn = f"oc.classname = '{oc_name}'"
                whrs_oc = WhereElements(
                    WhereElement(condition = cndtn))
                create_tileset(args, output_folder=oc_folder, max_features_per_tile=oc_mfpt, whrs=whrs_oc)
    else:
        advises = read_yaml(args.output, "advise.yml")
        create_tileset(args, output_folder=args.output, max_features_per_tile=advises["max_features"])