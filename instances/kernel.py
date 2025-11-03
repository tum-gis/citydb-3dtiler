#External Libraries
import sys

# Insert the folders to the SYS Environment
sys.path.insert(0, "../classes")

# Internal Libraries
from sql_blocks import *

def set_kernel():
    # SELECT st_transform(gmdt.geom, 4979) FROM geometry_data as gmdt
    slct = SelectElement("field", "st_transform(gmdt.geom)", alias="geom")
    frm = FromElement(table="geometry_data", alias="gmdt")
    qryblck = QueryBlock("kernel", "gmdt", "Spatial", 1, select_elements=[slct], from_elements=[frm])
    return qryblck