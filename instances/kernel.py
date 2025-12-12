#External Libraries
import sys

# Internal Libraries
from classes.sql_blocks import *

krnl_selects = SelectElements(
    SelectElement(
        select_type = "field", 
        field = "st_transform(gmdt.geometry,4979)", 
        range_alias="geom"),
    SelectElement(
        select_type = "field", 
        field = "objectid", 
        domain_alias="ftr", 
        range_alias="id"),
    SelectElement(
        select_type = "field", 
        field = "classname", 
        domain_alias="oc", 
        range_alias="class"),
    SelectElement(
        select_type = "field", 
        field = "alias",
        domain_alias = "ns",
        range_alias = "ns"),
    distinct_on = "gmdt.id" #,
    # Concatenated alternative for the classname and the namespace alias
    # SelectElement(
    #     select_type = "field",
    #     field = "CONCAT(ns.alias,'__',oc.classname)",
    #     range_alias = "class2")
    )
krnl_froms = FromElements(
    FromElement(
        table="geometry_data", 
        alias="gmdt")
    )
krnl_joins = JoinElements(
    JoinElement(
        join_type= "left", 
        table="feature", 
        range_alias="ftr", 
        condition="ftr.id = gmdt.feature_id"),
    JoinElement(
        join_type= "left", 
        table="objectclass", 
        range_alias="oc", 
        condition="oc.id = ftr.objectclass_id"),
    JoinElement(
        join_type="left",
        table="namespace",
        range_alias="ns",
        condition="oc.namespace_id = ns.id")
    )
krnl_query = QueryBlock(
    name = "kernel", 
    type_of_effect = "Spatial",
    order_number =  1, 
    range_alias = "gmdt",
    select_elements=krnl_selects, 
    from_elements=krnl_froms, 
    join_elements=krnl_joins)