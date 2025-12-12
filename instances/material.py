#External Libraries
import sys

# Internal Libraries
from classes.sql_blocks import *

# Necessary Selects and Joins for the Objectclass-based Styling

sl_no_material = SelectElement(
    select_type = "field", 
    field = "nmt.material_data", 
    range_alias = "material_data"
    )

sl_material_by_objectclass_fd = SelectElement(
    select_type = "field",
    field = "COALESCE(mtr_oc.material_data, nmt.material_data)",
    range_alias = "material_data"
    )

jn_no_material = JoinElement(
    join_type = "left",
    table = "vw_material_by_objectclass",
    range_alias = "nmt",
    condition = "nmt.ns is NULL AND nmt.class = 'anything_else'"
    )

jn_material_by_objectclass = JoinElement(
    join_type = "left",
    table = "vw_material_by_objectclass",
    range_alias = "mtr_oc",
    condition = "mtr_oc.ns = ns.alias AND mtr_oc.class = oc.classname" # Check kernel
    )

# Neccassary Selects, Joins and QueryBlocks for the Attribute-based Styling


sl_material_by_property_fd = SelectElement(
    select_type = "field",
    field = "COALESCE(mtr_prp_mtc.material_data, COALESCE(mtr_oc.material_data, nmt.material_data))",
    range_alias = "material_data"
    )

jn_material_by_properties = JoinElement(
    join_type = "left",
    table = "vw_material_by_properties_matches",
    range_alias = "mtr_prp_mtc",
    condition = "mtr_prp_mtc.objectid = ftr.objectid" 
    )