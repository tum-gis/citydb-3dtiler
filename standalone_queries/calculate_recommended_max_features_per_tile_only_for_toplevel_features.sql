-- Calculate Recommended Max Features Per Tile
-- Only For Top-Level Features
 -- SELECTED MAX_POINTS value is 10K

SELECT avg_vertice_number,
       min_vertice_number,
       max_vertice_number,
       ROUND(10000/avg_vertice_number) AS max_features_per_tile
FROM
    (SELECT AVG(st_npoints(gd.geometry)) AS avg_vertice_number ,
            MAX(st_npoints(gd.geometry)) AS max_vertice_number ,
            MIN(st_npoints(gd.geometry)) AS min_vertice_number ,
            count(gd.id)
     FROM geometry_data as gd
     LEFT JOIN feature as ftr ON
        ftr.id = gd.feature_id
     LEFT JOIN objectclass as oc ON
        oc.id = ftr.objectclass_id
     WHERE oc.is_toplevel > 0);