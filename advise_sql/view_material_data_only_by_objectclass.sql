-- View: citydb.material_data_only_by_objectclass
 -- DROP VIEW citydb.material_data_only_by_objectclass;

CREATE OR REPLACE VIEW citydb.material_data_only_by_objectclass AS
SELECT namespace_of_classname,
       classname,
       JSON_OBJECT(
            'EmissiveColors' : NULLIF(ARRAY[pbr_emmisive_color], '{NULL}'), 
            'PbrMetallicRoughness' : pbr_metallic_roughness, 
            'SpecularGlossiness' : NULLIF(pbr_specular_glossiness, '{}')
            ABSENT ON NULL RETURNING json)
            AS material_data
FROM
    (SELECT mtf.namespace_of_classname,
            mtf.classname,
            mtf.emmisive_color as pbr_emmisive_color,
            json_object(
                'BaseColors' : NULLIF(ARRAY[mtf.pbr_metallic_roughness_base_color], '{NULL}'), 
                'MetallicRoughness' : NULLIF(ARRAY[mtf.pbr_metallic_roughness_metallic_roughness], '{NULL}')
                ABSENT ON NULL RETURNING json)::json
                AS pbr_metallic_roughness,
             jsonb_strip_nulls(json_object(
                'DiffuseColors' : NULLIF(ARRAY[mtf.pbr_specular_glossiness_diffuse_color], '{NULL}'), 
                'SpecularGlossiness' : NULLIF(ARRAY[mtf.pbr_specular_glossiness_specular_glossiness], '{NULL}') 
                 NULL ON NULL RETURNING json)::jsonb)
                 AS pbr_specular_glossiness
     FROM materials_for_features as mtf
     WHERE mtf.property_value IS NULL);


ALTER TABLE citydb.material_data_only_by_objectclass OWNER TO tester;

