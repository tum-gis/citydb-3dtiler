-- View: citydb.vw_material_by_properties
 -- DROP VIEW citydb.vw_material_by_properties;

CREATE OR REPLACE VIEW citydb.vw_material_by_properties AS
SELECT namespace_of_classname,
       classname,
       namespace_of_property,
       property_name,
       column_name_of_property_value,
       property_value,
       JSON_OBJECT(
            'EmissiveColors' : emmisive_color, 
            'PbrMetallicRoughness' : pbr_metallic_roughness, 
            'SpecularGlossiness' : pbr_specular_glossiness 
            ABSENT ON NULL RETURNING json
            ) AS material_data
FROM
    (SELECT m.namespace_of_classname,
            m.classname,
            m.namespace_of_property,
            m.property_name,
            m.column_name_of_property_value,
            m.property_value,
            m.emmisive_color,
            json_object(
                'BaseColors' : NULLIF(ARRAY[m.pbr_metallic_roughness_base_color], '{NULL}'), 
                'MetallicRoughness' : NULLIF(ARRAY[m.pbr_metallic_roughness_metallic_roughness], '{NULL}')
                ABSENT ON NULL RETURNING json)::json
                AS pbr_metallic_roughness,
            jsonb_strip_nulls(json_object(
                'DiffuseColors' : NULLIF(ARRAY[m.pbr_specular_glossiness_diffuse_color], '{NULL}'), 
                'SpecularGlossiness' : NULLIF(ARRAY[m.pbr_specular_glossiness_specular_glossiness], '{NULL}') 
                 NULL ON NULL RETURNING json)::jsonb)
                 AS pbr_specular_glossiness
     FROM _materials_for_features as m) pbr_1;


ALTER TABLE citydb.vw_material_by_properties OWNER TO tester;

