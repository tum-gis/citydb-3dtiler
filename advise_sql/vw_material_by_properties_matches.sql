SELECT 
   DISTINCT ON (gmdt.id) 
   st_transform(gmdt.geometry,4979) AS geom,
   ftr.objectid AS id,
   oc.classname AS CLASS,
   ns.alias AS ns,
   COALESCE(mtr_prp_mtc.material_data, COALESCE(mtr_oc.material_data, nmt.material_data)) AS material_data
FROM geometry_data AS gmdt
LEFT  JOIN feature AS ftr ON ftr.id = gmdt.feature_id
LEFT  JOIN objectclass AS oc ON oc.id = ftr.objectclass_id
LEFT  JOIN namespace AS ns ON oc.namespace_id = ns.id

LEFT JOIN vw_material_by_properties_matches as mtr_prp_mtc ON
    mtr_prp_mtc.objectid = ftr.objectid

LEFT  JOIN vw_material_by_objectclass AS mtr_oc ON mtr_oc.ns = ns.alias
AND mtr_oc.class = oc.classname
LEFT  JOIN vw_material_by_objectclass AS nmt ON 
    nmt.ns IS NULL AND nmt.class = 'anything_else'