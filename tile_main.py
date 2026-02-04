#External Libraries
import sys
import os

# Internal Libraries
from io_tools.yaml import write_yaml
from io_tools.folder import create_folder, check_custom_materials
from io_tools.yaml import read_yaml
from io_tools.tiles import generate_tiles
from io_tools.pg_plpgsql import copy_materials, drop_cascade_if_exists
from io_tools.pg_sql import read_sql_file
from database.pg_connection import run_sql
from classes.sql_blocks import *
from instances.kernel import krnl_query
from instances.material import no_style_query, objectclass_falldown_query, custom_property_falldown_query
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql
from default_paths import get_base_path, get_shared_folder_path

# Set the default path of the shared folder
shared_folders_path = os.path.join(os.getcwd(), "shared")

def create_tileset(args, output_path=None, max_features_per_tile=None, whrs=None):
    # Drop the materials table if it is existing in DB
    drop_cascade_if_exists(args, "_materials_for_features")
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

    # !Refactor the following code blcok!
    # Set the controller for the materials
    if args.style_mode == "no-style" and args.style_absence_behavior == 'fall-down':
        # If any filter is given, add the filter to the query
        if whrs != None:
            no_style_query[0].where_elements = whrs
        query = str(no_style_query)

        # Find the geom column in the Select Elements
        for sl in no_style_query.select_elements:
            if sl.range_alias == 'geom':
                geom_col_idx = list(no_style_query.select_elements).index(sl)
        geom_col = str(no_style_query.select_elements[geom_col_idx].range_alias)

        # Find the shaders column in the Select Elements
        for sl in no_style_query.select_elements:
            if sl.range_alias == 'material_data':
                shaders_col_idx = list(no_style_query.select_elements).index(sl)
        shaders_col = str(no_style_query.select_elements[shaders_col_idx].range_alias)

    elif args.style_mode == 'objectclass-based' and args.style_absence_behavior == 'fall-down':
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
    #Test
    print(str(query))
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, geom_col)
    # print(crt_mv)
    run_sql(args, crt_mv, name=f"create_materialized_view (function) for {mv_name}")
    run_sql(args, ind_mv, name=f"index_materialized_view (function) for {mv_name}")
    generate_tiles(args, mv_name, geom_col, shaders_col, output_path, mfpt)

def tile(args):
    print(args.separate_tilesets)
    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            advises = read_yaml(get_shared_folder_path(), "advise.yml")
            objectclasses = advises["objectclasses"]
            
            for oc in objectclasses:
                oc_name = oc["name"]
                oc_mfpt = oc["objectclass_recommendations"]
                if args.output_folder == "shared":
                    # print("ok ok ok , here we are : ", new)
                    oc_path = create_folder(get_shared_folder_path(), oc_name)
                    #oc_path = os.path.join(new_folder, oc_name)
                else:
                    custom_path = os.path.join(get_shared_folder_path(), args.output_folder)
                    oc_path = create_folder(custom_path, oc_name)
                    #oc_path = os.path.join(custom_path, oc_name)
                
                # Set a Where condition for each calculator query that filters objectclasses
                cndtn = f"oc.classname = '{oc_name}'"
                whrs_oc = WhereElements(
                    WhereElement(condition = cndtn))
                # print("HERE IS THE PATH:", oc_path)
                create_tileset(args, output_path=oc_path, max_features_per_tile=oc_mfpt, whrs=whrs_oc)
    else:
        if args.output_folder == "shared":
            advises = read_yaml(get_shared_folder_path(), "advise.yml")
            tileset_path = get_shared_folder_path()
        else:
            custom_path = os.path.join(get_shared_folder_path(), args.output_folder)
            advises = read_yaml(get_shared_folder_path(), "advise.yml")
            tileset_path = custom_path
        create_tileset(args, output_path=tileset_path, max_features_per_tile=advises["max_features"])