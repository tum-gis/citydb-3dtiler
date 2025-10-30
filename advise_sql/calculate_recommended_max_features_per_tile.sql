-- Calculate Recommended Max Features Per Tile
 -- SELECTED MAX_POINTS value is 10K

SELECT avg_vertice_number,
       min_vertice_number,
       max_vertice_number,
       ROUND(10000/avg_vertice_number) AS max_features_per_tile
FROM
    (SELECT AVG(st_npoints(geometry)) AS avg_vertice_number ,
            MAX(st_npoints(geometry)) AS max_vertice_number ,
            MIN(st_npoints(geometry)) AS min_vertice_number ,
            count(id)
     FROM geometry_data);