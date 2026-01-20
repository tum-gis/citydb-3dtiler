-- View: citydb.vw_material_by_properties_matches

-- DROP VIEW citydb.vw_material_by_properties_matches;

CREATE OR REPLACE VIEW citydb.vw_material_by_properties_matches
 AS
 SELECT ftr.objectid,
    prp_ns.alias,
    prp.name,
    prp.val_string,
    prp.val_int,
    prp.val_double,
    mtr_prp.material_data
   FROM feature ftr
     LEFT JOIN objectclass oc ON oc.id = ftr.objectclass_id
     LEFT JOIN namespace ns ON ns.id = oc.namespace_id
     LEFT JOIN property prp ON prp.feature_id = ftr.id
     LEFT JOIN namespace prp_ns ON prp_ns.id = prp.namespace_id
     JOIN vw_material_by_properties mtr_prp ON mtr_prp.namespace_of_classname = ns.alias AND mtr_prp.classname = oc.classname AND mtr_prp.namespace_of_property = prp_ns.alias AND mtr_prp.property_name = prp.name AND (mtr_prp.property_value = prp.val_string OR mtr_prp.property_value = prp.val_int::text OR mtr_prp.property_value = prp.val_double::text);
