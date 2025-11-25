#External Libraries
import sys

# Internal Libraries
from classes.sql_blocks import *
from database.pg_connection import get_query_results

# Group of Geometry Statistics (Min, Max, Average, Total number of points per feature geometry):

selects1 = SelectElements(
        SelectElement(
            select_type="field",
            field="MIN(st_npoints(gd.geometry))",
            range_alias="min_vertices"),
        SelectElement(
            select_type="field",
            field="MAX(st_npoints(gd.geometry))",
            range_alias="max_vertices"), 
        SelectElement(
            select_type="field",
            field="AVG(st_npoints(gd.geometry))",
            range_alias="avg_vertices"), 
        SelectElement(
            select_type="field",
            field="count(gd.id)",
            range_alias="geometries_total")
        )
forms1 = FromElements(
        FromElement(
            table="geometry_data",
            alias="gd"
        )
    )
statistics_of_geometries = QueryBlock(
    name="Statistics of Geometries",
    range_alias="stt",
    type_of_effect="Spatial",
    order_number=1,
    select_elements=selects1,
    from_elements=forms1
    )

# Additional Group of Objectclass based separation (Separates the statistics by conisdering objectclasses)

joins3 = JoinElements(
    JoinElement(
        join_type = "left",
        table = "feature",
        range_alias = "ftr",
        condition = "ftr.id = gd.feature_id"
        ), 
    JoinElement(
        join_type = "left",
        table = "objectclass",
        range_alias = "oc",
        condition = "ftr.objectclass_id = oc.id"
        )
    )
# wheres3 = WhereElements(
#     WhereElement(
#         condition = "oc.classname = 'Building'"
#         )
#     )
addition_of_objectclasses = QueryBlock(
    name = "Addition of Objectclasses",
    type_of_effect = "Ontological",
    order_number = 2,
    join_elements = joins3#,
    # where_elements = wheres3
    )

# Combination of "Statistics of Geometries" and "Addition of Objectclasses"

qryblcks = QueryBlocks(statistics_of_geometries, addition_of_objectclasses)
statistics_of_geometries_w_objectclasses = CompositeQueryBlock(
    name = "Statistics of Geometries by every Objectclasses",
    db_type = "postgresql",
    query_blocks = qryblcks)

# Group of Recommended Maximum Features Per Tile (encapsulates Geometry Statistics)

selects2 = SelectElements(
        SelectElement(
            select_type="field",
            field="min_vertices"
            ), 
        SelectElement(
            select_type="field",
            field="max_vertices"
            ), 
        SelectElement(
            select_type="field",
            field="avg_vertices"
            ), 
        SelectElement(
            select_type="field",
            field = "ROUND(10000/avg_vertices)",
            range_alias = "max_features_per_tile"
        )
    )
forms2 = FromElements(
    FromElement(
        inner_query_blocks = [statistics_of_geometries_w_objectclasses])
    )
recommended_max_features_per_tile = QueryBlock(
    name = "Recommended Max Features Per Tile",
    type_of_effect = "Spatial",
    order_number = 1,
    select_elements = selects2,
    from_elements = forms2
    )