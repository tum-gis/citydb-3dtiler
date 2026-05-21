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
from database.pg_connection import run_sql, get_query_results
from classes.sql_blocks import *
from instances.kernel import krnl_query
from instances.material import *
from instances.attributes import qry_blck_pro_shll, pro_prnt_selects, qry_blck_pro_prnt # QueryBlock of the Shell query of Joins
from instances.nested_attributes import qry_blck_pro_nstd_shll1, qry_blck_pro_nstd_shll2, qry_blck_pro_nstd_add, cmb_pro_nstd
from database.pg_connection import create_materialized_view, index_materialized_view, get_query_results, run_sql
from default_paths import get_base_path, get_shared_folder_path

# Set the default path of the shared folder
shared_folders_path = os.path.join(os.getcwd(), "shared")

def selected_attributes_to_list(selected_attributes):
    attributes_list = selected_attributes.split(",")
    return attributes_list

def create_tileset(args, output_path=None, max_features_per_tile=None, whrs=None, attribute_list = None):
    # print("-o-o-o-o-o>>", attribute_list)
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
    crt_vw_mat_exstng, crt_vw_mat_exstng_fl_nm = read_sql_file("standalone_queries", "vw_material_as_existing_app.sql")
    run_sql(args, crt_vw_mat_exstng, name=crt_vw_mat_exstng_fl_nm)

    # No
    # Set the controller for the materials
    if args.style_mode == "no-style" and args.style_absence_behavior == 'fall-down':
        # If any filter is given, add the filter to the query
        if whrs != None:
            no_styling_addition.where_elements = whrs
        selected_styling_addition = no_styling_addition
    elif args.style_mode == "no-style" and args.style_absence_behavior == 'rise-up':
        raise ValueError('"No-Style" mode can not be used with the "rise-up" option.')
    elif args.style_mode == 'objectclass-based' and args.style_absence_behavior == 'fall-down':
        # If any filter is given, add the filter to the query
        if whrs != None:
            objectclass_falldown_addition.where_elements = whrs
        # print(objectclass_falldown_addition)
        selected_styling_addition = objectclass_falldown_addition
    elif args.style_mode == 'property-based' and args.style_absence_behavior == 'fall-down':
        # If any filter is given, add the filter to the query
        if whrs != None:
            properties_falldown_addition.where_elements = whrs
        selected_styling_addition = properties_falldown_addition
    elif args.style_mode == 'existing-appearances' and args.style_absence_behavior == 'fall-down':
        # If any filter is given, add the filter to the query
        if whrs != None:
            existing_app_falldown_addition.where_elements = whrs
        selected_styling_addition = existing_app_falldown_addition
    elif args.style_mode == 'existing-appearances' and args.style_absence_behavior == 'rise-up':
        raise Exception('"Existing-appearances" mode can not be used with the "rise-up" option.')
    elif args.style_mode == 'objectclass-based' and args.style_absence_behavior == 'rise-up':
        # If any filter is given, add the filter to the query
        if whrs != None:
            objectclass_riseup_addition.where_elements = whrs
        selected_styling_addition = objectclass_riseup_addition
    elif args.style_mode == 'property-based' and args.style_absence_behavior == 'rise-up':
        # If any filter is given, add the filter to the query
        if whrs != None:
            properties_riseup_addition.where_elements = whrs
        selected_styling_addition = properties_riseup_addition

    if args.vertical_offset != "0.0":
        offs = float(args.vertical_offset)
        # The first element in the SelectElements is geometry col. in kernel query.
        krnl_query.select_elements[0].field = f"st_translate(gmdt.geometry, 0, 0, {offs})"

    # Set the attributes in the following parts considering the relevant arguments.
    if args.attributes == 'none':
        print("(info): None of the attributes selected.")
        query = QueryBlocks(krnl_query, selected_styling_addition)
        attribute_as_string = None
    elif args.attributes == 'selected':
        attribute_list = selected_attributes_to_list(args.selected_attributes)
        # Following Queries will be used for the flat structure option
        if args.attribute_structure == 'flat':
            attr_slcts = SelectElements()
            attr_joins = JoinElements()
            for attr in attribute_list:
                attr_slct = SelectElement(
                    field = "pro_value",
                    domain_alias = attr,
                    range_alias = attr,
                    coalesce = '-NA-'
                    )
                attr_join = JoinElement(
                    inner_query_block = qry_blck_pro_shll,
                    range_alias = attr,
                    condition = attr + ".feature_id = ftr.id AND LOWER("+attr+".pro_name) = '"+ attr +"'"
                    )
                attr_slcts.add(attr_slct)
                attr_joins.add(attr_join)
                # print("HERE--->:\n", attr_joins)
            selected_attribute_addition = QueryBlock(
                name = "selected attribute joins",
                type_of_effect = "semantic",
                order_number = 3,
                select_elements = attr_slcts,
                join_elements = attr_joins
                )
            query = QueryBlocks(krnl_query, selected_styling_addition, selected_attribute_addition)
            attribute_as_string = args.selected_attributes
            attribute_as_string = attribute_as_string.lower()
        elif args.attribute_structure == 'nested':
            attr_slcts = SelectElements()
            attr_joins = JoinElements()
            for attr in attribute_list:
                attr_slct = SelectElement(
                    field = "pro_value",
                    domain_alias = attr,
                    range_alias = attr,
                    coalesce = "{}"
                    )
                attr_join = JoinElement(
                    inner_query_block = cmb_pro_nstd,
                    range_alias = attr,
                    condition = attr + ".feature_id = ftr.id AND LOWER("+attr+".pro_name) = '"+ attr +"'"
                    )
                attr_slcts.add(attr_slct)
                attr_joins.add(attr_join)
                # print("HERE--->:\n", attr_joins)
            selected_attribute_addition_as_nested = QueryBlock(
                name = "selected attribute joins as nested",
                type_of_effect = "semantic",
                order_number = 3,
                select_elements = attr_slcts,
                join_elements = attr_joins
                )
            query = QueryBlocks(krnl_query, selected_styling_addition, selected_attribute_addition_as_nested)
            attribute_as_string = args.selected_attributes
            attribute_as_string = attribute_as_string.lower()
            # print(cmb_pro_nstd)

    elif args.attributes == 'all':
        attr_slcts = SelectElements()
        attr_joins = JoinElements()
        # Remove the redundant values (such as core_name) from the list:
        attr_list = list(set(attribute_list))
        # Remove the None values from the list
        attr_list = list(filter(lambda x: x is not None, attr_list))
        if len(attr_list) > 0:
            if args.attribute_structure == 'flat':
                for attr in attr_list:
                    attr_slct = SelectElement(
                        field = "pro_value",
                        domain_alias = attr,
                        range_alias = attr,
                        coalesce = '-NA-'
                        )
                    attr_join = JoinElement(
                        inner_query_block = qry_blck_pro_shll,
                        range_alias = attr,
                        condition = attr + ".feature_id = ftr.id AND LOWER("+attr+".pro_name) = '"+ attr +"'"
                        )
                    attr_slcts.add(attr_slct)
                    attr_joins.add(attr_join)
                all_attribute_addition = QueryBlock(
                    name = "all attribute joins",
                    type_of_effect = "semantic",
                    order_number = 3,
                    select_elements = attr_slcts,
                    join_elements = attr_joins
                    )
                query = QueryBlocks(krnl_query, selected_styling_addition, all_attribute_addition)
                attribute_as_string = ",".join(attr_list)
                attribute_as_string = attribute_as_string.lower()
            elif args.attribute_structure == 'nested':
                for attr in attr_list:
                    attr_slct = SelectElement(
                        field = "pro_value",
                        domain_alias = attr,
                        range_alias = attr,
                        coalesce = '{}'
                        )
                    attr_join = JoinElement(
                        inner_query_block = cmb_pro_nstd,
                        range_alias = attr,
                        condition = attr + ".feature_id = ftr.id AND LOWER("+attr+".pro_name) = '"+ attr +"'"
                        )
                    attr_slcts.add(attr_slct)
                    attr_joins.add(attr_join)
                all_attribute_addition_as_nested = QueryBlock(
                    name = "all attribute joins",
                    type_of_effect = "semantic",
                    order_number = 3,
                    select_elements = attr_slcts,
                    join_elements = attr_joins
                    )
                query = QueryBlocks(krnl_query, selected_styling_addition, all_attribute_addition_as_nested)
                attribute_as_string = ",".join(attr_list)
                attribute_as_string = attribute_as_string.lower()
        else:
            query = QueryBlocks(krnl_query, selected_styling_addition)
            attribute_as_string = None
    

    # Set the name of materialized view that would be used for tiling
    mv_name = "mv_geometries"
    mfpt = max_features_per_tile

    #Test
    # print("--->", query)
    
    crt_mv = create_materialized_view(mv_name, str(query))
    ind_mv = index_materialized_view(mv_name, 'geom')
    # print(crt_mv)
    run_sql(args, crt_mv, name=f"create_materialized_view (function) for {mv_name}")
    run_sql(args, ind_mv, name=f"index_materialized_view (function) for {mv_name}")
    generate_tiles(args, mv_name, 'geom', 'material_data', output_path, mfpt, attribute_as_string)

def summarize_advice(args):
    advices = read_yaml(get_shared_folder_path(), "advice.yml")
    objectclasses = advices["objectclasses"]
    mx_ftr_pr_tl = advices["max_features"]
    oc_attrs = []
    for oc in objectclasses:
        pros = oc["properties"]
        for pro in pros:
            oc_attrs.append(pro)
    return { "objectclasses": objectclasses, "attribute_list": oc_attrs, "max_features_per_tile": mx_ftr_pr_tl }

def tile(args):
    # print(args.separate_tilesets)
    if args.separate_tilesets is not None:
        if args.separate_tilesets == "objectclass":
            # advises = read_yaml(get_shared_folder_path(), "advice.yml")
            # objectclasses = advises["objectclasses"]
            advice_summary = summarize_advice(args)
            objectclasses = advice_summary["objectclasses"]
            for oc in objectclasses:
                oc_name = oc["name"]
                oc_mfpt = oc["objectclass_recommendations"]
                oc_attrs = oc["properties"]

                # Convert the property names to the lower characters (necessary for SQL)
                oc_attrs2 = []
                for attr in oc_attrs:
                    if attr is not None:
                        oc_attrs2.append(attr.lower())
                # oc_attrs = [x.lower() for x in oc_attrs]
                if args.output_folder == "shared":
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
                # print("HERE IS THE WHERE COND:", whrs_oc)
                create_tileset(args, output_path=oc_path, max_features_per_tile=oc_mfpt, whrs=whrs_oc, attribute_list = oc_attrs2)
    else:
        advice_summary = summarize_advice(args)
        if args.output_folder == "shared":
            tileset_path = get_shared_folder_path()
        else:
            custom_path = os.path.join(get_shared_folder_path(), args.output_folder)
            tileset_path = custom_path
        create_tileset(args, output_path=tileset_path, max_features_per_tile=advice_summary["max_features_per_tile"], attribute_list = advice_summary["attribute_list"])