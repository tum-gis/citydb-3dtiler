# Internal Libraries
from classes.sql_blocks import *
from .attributes import qry_blck_pro_prnt

# This file is dedicated to retrieve the only attributes
#   in nested/json-like format.

# SHELL I (Gathers all the children elements as row)

# pro.id, pro.name, ns.alias, krnl.id, krnl.feature_id, prnt_name
#   RELAVANT VALUE COLUMN (CASE)

# if the datatype is one of the given types then use 
#  the relavant  "val_" column from the database.
pro_rlvnt_val_cs = CaseElements(
    CaseElement(
        condition = "pro.datatype_id = 2", # Boolean
        result = "pro.val_int::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 3", # Integer
        result = "pro.val_int::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 4", # Double
        result = "pro.val_double::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 5", # String
        result = "pro.val_string::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 6", # URI
        result = "pro.val_uri::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 7", # Timestamp
        result = "pro.val_timestamp::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 14", # Code
        result = "pro.val_string::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 17", # Measure
        result = "pro.val_double::text"
        )
    )

pro_shll1_slcts = SelectElements(
    SelectElement(
        field = "id",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "name",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "alias",
        domain_alias = "ns"
        ),
    SelectElement(
        field = "id",
        domain_alias = "krnl",
        range_alias = "krnl_id"
        ),
    SelectElement(
        field = "feature_id",
        domain_alias = "krnl"
        ),
    SelectElement(
        field = "CONCAT(krnl.alias, '_', krnl.name)",
        range_alias = "prnt_name"
        ),
    SelectElement(
        select_type = "case",
        case = pro_rlvnt_val_cs,
        range_alias = "pro_value"
        )
    )

pro_shll1_frms = FromElements(
    FromElement(
        table = "property",
        alias = "pro"
        )
    )

# Here the parent properties joined as inner query
pro_shll1_jns = JoinElements(
    JoinElement(
        table = "namespace",
        range_alias = "ns",
        condition = "ns.id = pro.namespace_id"
        ),
    JoinElement(
        inner_query_block = qry_blck_pro_prnt,
        range_alias = "krnl",
        condition = "krnl.id = pro.parent_id"
        )
    )

# Only the interested datatypes (see lines 90-127) have been used 
#   to filter the results.
# 2:Boolean, 3:Integer, 4:Double, 5:String, 6:URI, 7:TimeStamp, 
# 12:Reference, 14:Code, 15:ExternalReference, 17:Measure, 
# 20:QualifiedArea, 21:QualifiedVolume
# 19:Occupancy, 102:SensorConnection, 200:GenericAttributeSet, 
# 700:ConstructionEvent, 701:Elevation, 702:Height, 900:RoomHeight
pro_shll1_whrs = WhereElements(
    WhereElement(
        condition = "pro.datatype_id IN (2,3,4,5,6,7,12,14,15,17,20,21) AND pro.parent_id IS NOT NULL"
        )
    )

qry_blck_pro_nstd_shll1 = QueryBlocks(
    QueryBlock(
        name = "Property Join for Nested Attributes (Shell I)",
        type_of_effect = "semantic",
        order_number = 1, # it is not a certain number
        select_elements = pro_shll1_slcts,
        from_elements = pro_shll1_frms,
        join_elements = pro_shll1_jns,
        where_elements = pro_shll1_whrs,
        range_alias = "shll"
        )
    )

# Shell I ends here

# Shell II (Aggregates the children elements retrieved from the Shell I)

pro_shll2_slcts = SelectElements(
    SelectElement(
        field = "krnl_id",
        domain_alias = "shll",
        range_alias = "id"
        ),
    SelectElement(
        field = "feature_id",
        domain_alias = "shll"
        ),
    SelectElement(
        field = "prnt_name",
        domain_alias = "shll",
        range_alias = "pro_name"
        ),
    SelectElement(
        field = "json_objectagg(CONCAT(shll.alias, '_', shll.name) : shll.pro_value)",
        range_alias = "pro_value"
        )
    )

pro_shll2_frms = FromElements(
    FromElement(
        inner_query_blocks = qry_blck_pro_nstd_shll1
        )
    )

pro_shll2_grps = GroupElements(
    GroupElement(
        field = "shll.krnl_id"
        ),
    GroupElement(
        field = "shll.prnt_name"
        ),
    GroupElement(
        field = "shll.feature_id"
        )
    )

qry_blck_pro_nstd_shll2 = QueryBlock(
    name = "Property Join for Nested Attributes (Shell II)",
    type_of_effect = "semantic",
    order_number = 1, # it is not a certain number
    select_elements = pro_shll2_slcts,
    from_elements = pro_shll2_frms,
    group_elements = pro_shll2_grps
    )

# Shell II ends here

# Additional part of the normal attributes
# This part will be combined with the nested attributes, but
# differently (from the flat attributes scenario) as json values.

# Add I starts here

pro_add_slcts = SelectElements(
    SelectElement(
        field = "id",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "feature_id",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "CONCAT(ns.alias, '_', pro.name)",
        range_alias = "pro_name"
        ),
    SelectElement(
        select_type = "case",
        case = pro_rlvnt_val_cs,
        range_alias = "pro_value",
        converter = "TO_JSON"
        )
    )

pro_add_frms = FromElements(
    FromElement(
        table = "property",
        alias = "pro"
        )
    )

pro_add_jns = JoinElements(
    JoinElement(
        table = "namespace",
        range_alias = "ns",
        condition = "ns.id = pro.namespace_id"
        )
    )

pro_add_whrs = WhereElements(
    WhereElement(
        condition = "pro.datatype_id IN (2,3,4,5,6,7,12,14,15,17,20,21) AND pro.parent_id IS NULL"
        )
    )

qry_blck_pro_nstd_add = QueryBlock(
    name = "Property Join for Nested Attributes (Addition for normal attributes)",
    type_of_effect = "semantic",
    order_number = 2, # not used
    select_elements = pro_add_slcts,
    from_elements = pro_add_frms,
    join_elements = pro_add_jns,
    where_elements = pro_add_whrs
    )

# Add I ends here

# Combination fo the Shell II and Addition I will create the query for
#  the nested attributes as JSON fields

# Comb I starts here

cmb_pro_nstd = CombinationElement(
    name = "Combines ordinary attributes with nested attributes as JSON",
    range_alias = "nstd_pro",
    type_of_effect = "semantic",
    order_number = 1,
    domain_query = qry_blck_pro_nstd_shll2,
    range_query = qry_blck_pro_nstd_add,
    type = "UNION",
    is_all = True
    )