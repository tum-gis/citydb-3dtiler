-- Get all the available objectclasses in the database
-- including top-level and sub-level features

SELECT ARRAY_AGG(classname)
FROM
    (SELECT oc.classname
	 FROM geometry_data gd
     LEFT JOIN feature ftr ON ftr.id = gd.feature_id
     LEFT JOIN objectclass oc ON oc.id = ftr.objectclass_id
     GROUP BY oc.classname)