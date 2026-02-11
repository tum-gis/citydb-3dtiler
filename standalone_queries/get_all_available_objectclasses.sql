-- Get all the available objectclasses in the database
-- including top-level and sub-level features
-- with the existing properties

SELECT 
    json_object_agg(pros3.classname, pros3.properties)
FROM
(
SELECT
    pros2.classname,
    json_build_object('properties', json_agg(pros2.key)) as properties
FROM
    (
    SELECT 
        pros.classname,
        pros.key
    FROM 
        (
        SELECT 
            oc.classname,
            CASE
                WHEN NULLIF(CONCAT(ns2.alias, '__', pro2.name), '__') IS NULL
                    THEN NULLIF(CONCAT(ns.alias, '__', pro.name), '__')
                ELSE
                    CONCAT(ns2.alias, '__', pro2.name, '.', ns.alias, '__', pro.name) 
            END as key
        FROM feature as ftr
        LEFT JOIN objectclass as oc ON
            oc.id = ftr.objectclass_id
        LEFT JOIN property as pro ON
            pro.feature_id = ftr.id
            AND pro.datatype_id not in (10, 11) -- 'GeometryProperty', 'FeatureProperty'
        LEFT JOIN namespace as ns ON
            ns.id = pro.namespace_id
        LEFT JOIN datatype as dt ON
            dt.id = pro.datatype_id
        LEFT JOIN property as pro2 ON
            pro2.id = pro.parent_id
        LEFT JOIN namespace as ns2 ON
            ns2.id = pro2.namespace_id
        ) pros
    GROUP BY pros.classname, pros.key
    ORDER BY pros.classname ASC
    ) as pros2
GROUP BY pros2.classname
) as pros3



