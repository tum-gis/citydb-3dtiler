#External Libraries
import sys

# Internal Libraries
from classes.sql_blocks import *
from instances.kernel import *

# Neccassary Selects and Joins for the No-Style option

sl_material_w_no_styling = SelectElement(
    select_type = "field",
    field = "nmt.material_data",
    range_alias = "material_data"
    )

jn_no_material = JoinElement(
    join_type = "left",
    table = "vw_material_by_objectclass",
    range_alias = "nmt",
    condition = "nmt.ns is NULL AND nmt.class = 'anything_else'"
    )

no_styling_select_elements = SelectElements(sl_material_w_no_styling)
no_styling_join_elements = JoinElements(jn_no_material)

not_styling_addition = QueryBlock(
    name = "material_w_no_style", 
    type_of_effect = "Visual",
    order_number =  2, 
    select_elements=no_styling_select_elements, 
    join_elements=no_styling_join_elements
    )

no_style_query = QueryBlocks(krnl_query, not_styling_addition)

# Necessary Selects and Joins for the Objectclass-based Styling

# For nmt.material_data see above
sl_material_by_objectclass_fd = SelectElement(
    select_type = "field",
    field = "COALESCE(mtr_oc.material_data, nmt.material_data)",
    range_alias = "material_data"
    )

jn_material_by_objectclass = JoinElement(
    join_type = "left",
    table = "vw_material_by_objectclass",
    range_alias = "mtr_oc",
    condition = "mtr_oc.ns = ns.alias AND mtr_oc.class = oc.classname" # Check kernel
    )

objectclass_falldown_select_elements = SelectElements(sl_material_by_objectclass_fd)
# objectclass_falldown_join_elements = JoinElements(jn_material_by_objectclass, jn_no_material)
objectclass_falldown_join_elements = JoinElements(jn_material_by_objectclass, jn_no_material)

objectclass_falldown_addition = QueryBlock(
    name = "material_by_objectclass", 
    type_of_effect = "Visual",
    order_number =  2, 
    select_elements=objectclass_falldown_select_elements, 
    join_elements=objectclass_falldown_join_elements
    )

objectclass_falldown_query = QueryBlocks(krnl_query, objectclass_falldown_addition)


# Neccassary Selects, Joins and QueryBlocks for the Property-based Styling

sl_material_by_property_fd = SelectElement(
    select_type = "field",
    field = "COALESCE(mtr_prp_mtc.material_data, mtr_oc.material_data)",
    range_alias = "material_data"
    )

jn_material_by_properties = JoinElement(
    join_type = "left",
    table = "vw_material_by_properties_matches",
    range_alias = "mtr_prp_mtc",
    condition = "mtr_prp_mtc.objectid = ftr.objectid" 
    )

properties_falldown_select_elements = SelectElements(sl_material_by_property_fd)
# properties_falldown_join_elements = JoinElements(jn_material_by_properties, jn_material_by_objectclass, jn_no_material)
properties_falldown_join_elements = JoinElements(jn_material_by_properties, jn_material_by_objectclass)

properties_falldown_addition = QueryBlock(
    name = "material_by_properties", 
    type_of_effect = "Visual",
    order_number =  2, 
    select_elements=properties_falldown_select_elements, 
    join_elements=properties_falldown_join_elements
    )

custom_property_falldown_query = QueryBlocks(krnl_query, properties_falldown_addition)