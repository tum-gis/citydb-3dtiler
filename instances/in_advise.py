#External Libraries
import sys

# Internal Libraries
from classes.sql_blocks import *
from database.pg_connection import get_query_results

# Geometry Statistics (Min, Max, Average, Total number of points per feature geometry):

gmt_stt_selects = SelectElements(
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
            field="ROUND(AVG(st_npoints(gd.geometry)),2)",
            range_alias="avg_vertices"), 
        SelectElement(
            select_type="field",
            field="count(gd.id)",
            range_alias="geometries_total")
        )
gmt_stt_froms = FromElements(
        FromElement(
            table="geometry_data",
            alias="gd"
        )
    )

# Objectclass based separation (Separates the statistics by considering objectclasses)
oc_spr_joins = JoinElements(
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

geometry_statistics = QueryBlock(
    name = "Statistics of Geometries",
    range_alias = "stt",
    type_of_effect = "Spatial",
    order_number = 1,
    select_elements = gmt_stt_selects,
    from_elements = gmt_stt_froms,
    join_elements = oc_spr_joins
    )


# Combination of "Statistics of Geometries" and "Addition of Objectclasses"

# geometry_statistics_w_objectclasses = QueryBlock(
#     name = "Statistics of Geometries by every Objectclasses",
#     type_of_effect = "Ontological",
#     order_number = 1,
#     inner_query_blocks = geometry_statistics)

# Recommended Maximum Features Per Tile (encapsulates Geometry Statistics)

rcm_mxm_ftr_pr_tl_selects = SelectElements(
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
rcm_mxm_ftr_pr_tl_selects_froms = FromElements(
    FromElement(
        inner_query_blocks = [geometry_statistics])
    )
recommended_max_features_per_tile = QueryBlock(
    name = "Recommended Max Features Per Tile",
    type_of_effect = "Ontological",
    order_number = 1,
    select_elements = rcm_mxm_ftr_pr_tl_selects,
    from_elements = rcm_mxm_ftr_pr_tl_selects_froms
    )