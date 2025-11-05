#External Libraries
import sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "../classes")

# Internal Libraries
from sql_blocks import *

def set_kernel():
    # SELECT st_transform(gmdt.geom, 4979) FROM geometry_data as gmdt
    slct1 = SelectElement("field", "st_transform(gmdt.geometry,4979)", range_alias="geom")
    slct2 = SelectElement("field", "objectid", domain_alias="ftr", range_alias="id")
    slct3 = SelectElement("field", "classname", domain_alias="oc", range_alias="class")
    frm = FromElement(table="geometry_data", alias="gmdt")
    jn1 = JoinElement("left", table="feature", range_alias="ftr", condition="ftr.id = gmdt.feature_id")
    jn2 = JoinElement("left", table="objectclass", range_alias="oc", condition="oc.id = ftr.objectclass_id")
    qryblck = QueryBlock("kernel", "gmdt", "Spatial", 1, select_elements=[slct1, slct2, slct3], from_elements=[frm], join_elements=[jn1, jn2])
    #print(qryblck)
    return qryblck