# Internal Libraries
from classes.sql_blocks import *

# This part is dedicated to retrieve the only selected attributes
#   in flat/tabular format.

# The kernel query that requests the PARENT properties
# This query will be joined to the outer query to create the exact name
#   of the property like con_height__con_value (con_height is from parent)

# pro_prnt Selects:
# pro_krnl.id, pro_krnl.name, ns_krnl.alias
pro_prnt_selects = SelectElements(
    SelectElement(
        select_type = "field",
        field = "id",
        domain_alias = "pro_krnl"
    ),
    SelectElement(
        select_type = "field",
        field = "name",
        domain_alias = "pro_krnl"
    ),
    SelectElement(
        select_type = "field",
        field = "alias",
        domain_alias = "ns_krnl"
    )
)

# property as pro_krnl
pro_prnt_frms = FromElements(
    FromElement(
        table = "property",
        alias = "pro_krnl"
    )
)

# namespace as ns_krnl
pro_prnt_jns = JoinElements(
    JoinElement(
        table = "namespace",
        range_alias = "ns_krnl",
        condition = "ns_krnl.id = pro_krnl.namespace_id"
    )
)

# pro_krml.parent_id is NULL
pro_prnt_whrs = WhereElements(
    WhereElement(
        condition = "pro_krnl.parent_id is NULL"
    )
)

qry_blck_pro_prnt = QueryBlock(
    name = "parent property's namespace and name",
    range_alias = "pro_prnt",
    type_of_effect = "semantic",
    order_number = 1,
    select_elements = pro_prnt_selects,
    from_elements = pro_prnt_frms,
    join_elements = pro_prnt_jns,
    where_elements = pro_prnt_whrs
    )

# Kernel Query ends here

# Following query encapsulate the shell query for the attributes
#   This query will be used as the main JOIN for filtering the 
#   relavant attributes.

# pro.id, pro.parent_id, pro.feature_id, FULL-NAME of property (CASE),
#   RELAVANT VALUE COLUMN (CASE)

# if the property has a parent property use it's namespace and name
#   otherwise uwse only the name and namespace of itself
pro_shll_fll_nam_case = CaseElements(
        CaseElement(
            condition = "pro.parent_id is NULL",
            result = "CONCAT(ns_shll.alias, '_', pro.name)"
            ),
        CaseElement(
            else_result = "CONCAT(pro_prnt.alias, '_', pro_prnt.name, '__', ns_shll.alias, '_', pro.name)"
            )
    )

# if the datatype is one of the given types then use 
#  the relavant  "val_" column from the database.
pro_shll_rlvnt_val_case = CaseElements(
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
        ),
    CaseElement(
        condition = "pro.datatype_id = 701", # Elevation
        result = "pro.val_array::text"
        ),
    CaseElement(
        condition = "pro.datatype_id = 702", # Height
        result = "'none'::text"
        )
    )

pro_shll_slcts = SelectElements(
    SelectElement(
        field = "id",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "parent_id",
        domain_alias = "pro"
        ),
    SelectElement(
        field = "feature_id",
        domain_alias = "pro"
        ),
    SelectElement(
        select_type = "case",
        case = pro_shll_fll_nam_case,
        range_alias = "pro_name"
        ),
    SelectElement(
        select_type = "case",
        case = pro_shll_rlvnt_val_case,
        range_alias = "pro_value"
        )
    )

pro_shll_frms = FromElements(
    FromElement(
        table = "property",
        alias = "pro"
        )
    )

# Here the parent properties joined as inner query
pro_shll_jns = JoinElements(
    JoinElement(
        table = "namespace",
        range_alias = "ns_shll",
        condition = "ns_shll.id = pro.namespace_id"
        ),
    JoinElement(
        inner_query_block = qry_blck_pro_prnt,
        range_alias = "pro_prnt",
        condition = "pro_prnt.id = pro.parent_id"
        )
    )

# Only the interested datatypes (see lines 90-127) have been used 
#   to filter the results.
pro_shll_whrs = WhereElements(
    WhereElement(
        condition = "pro.datatype_id in (2,3,4,5,6,7,14,17,701,702)"
        )
    )

qry_blck_pro_shll = QueryBlock(
    name = "Property Join",
    #range_alias = "pro_shll",
    type_of_effect = "semantic",
    order_number = 10, # it is not a certain number
    select_elements = pro_shll_slcts,
    from_elements = pro_shll_frms,
    join_elements = pro_shll_jns,
    where_elements = pro_shll_whrs
    )

# Shell Query ends here