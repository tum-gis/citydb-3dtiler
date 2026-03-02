-- View: citydb.vw_material_as_existing_app
 -- DROP VIEW citydb.vw_material_as_existing_app;

CREATE OR REPLACE VIEW citydb.vw_material_as_existing_app AS
SELECT mtf_all.objectid,
       JSON_OBJECT(
	   	'EmissiveColors' : NULLIF(mtf_all.pbr_emmisive_color, '{NULL}'::text[]),
		'PbrMetallicRoughness' : mtf_all.pbr_metallic_roughness,
		'SpecularGlossiness' : NULLIF(mtf_all.pbr_specular_glossiness, '{}'::jsonb) ABSENT ON NULL RETURNING json) AS material_data
FROM
    (
	WITH dflt as (
			SELECT
				pbr_metallic_roughness_base_color as base_color,
				pbr_metallic_roughness_metallic_roughness as metallic_roughness
			FROM "_materials_for_features"
			WHERE classname = 'anything_else'
			)
	SELECT
		mtf_ea.objectid,
        mtf_ea.emmisive_color AS pbr_emmisive_color,
        JSON_OBJECT(
			'BaseColors' : COALESCE(NULLIF(mtf_ea.base_color, '{NULL}'::text[]), CONCAT('{',dflt.base_color,'}')::text[]),
			'MetallicRoughness' : COALESCE(NULLIF(mtf_ea.metallic_roughness, '{NULL}'::text[]), CONCAT('{',dflt.metallic_roughness,'}')::text[])
			ABSENT ON NULL RETURNING json)
		AS pbr_metallic_roughness,
        jsonb_strip_nulls(JSON_OBJECT('DiffuseColors' : NULLIF(mtf_ea.diffuse_color, '{NULL}'::text[]), 'SpecularGlossiness' : NULLIF(mtf_ea.specular_glossiness, '{NULL}'::text[]) ABSENT ON NULL RETURNING json)::jsonb) AS pbr_specular_glossiness
     FROM
         (
			--kernel started here
			SELECT
				krn1.objectid,
				ARRAY_AGG(krn1.base_color) FILTER (WHERE krn1.base_color is NOT NULL) as base_color,
				ARRAY_AGG(krn1.metallic_roughness) FILTER (WHERE krn1.metallic_roughness is NOT NULL) as metallic_roughness,
				ARRAY_AGG(krn1.emmisive_color) FILTER (WHERE krn1.emmisive_color is NOT NULL) as emmisive_color,
				ARRAY_AGG(krn1.diffuse_color) FILTER (WHERE krn1.diffuse_color is NOT NULL) as diffuse_color,
				ARRAY_AGG(krn1.specular_glossiness) FILTER (WHERE krn1.specular_glossiness is NOT NULL) as specular_glossiness
			FROM
			(
			SELECT
				ftr.objectid,
				sd.x3d_diffuse_color AS base_color,
				CASE
					WHEN sd.x3d_diffuse_color IS NOT NULL AND sd.x3d_shininess is NOT NULL AND sd.x3d_ambient_intensity is NOT NULL
					THEN CONCAT('#'::text,to_hex(round(sd.x3d_shininess*256)::integer)::text, to_hex(round(sd.x3d_ambient_intensity*256)::integer)::text, '00'::text)
					WHEN sd.x3d_diffuse_color IS NOT NULL AND sd.x3d_shininess is NOT NULL AND sd.x3d_ambient_intensity is NULL
					THEN CONCAT('#'::text,to_hex(round(sd.x3d_shininess*256)::integer)::text, '0000'::text)
					WHEN sd.x3d_diffuse_color IS NOT NULL AND sd.x3d_shininess is NULL AND sd.x3d_ambient_intensity is NOT NULL
					THEN CONCAT('#00'::text, to_hex(round(sd.x3d_ambient_intensity*256)::integer)::text, '00'::text)
					WHEN sd.x3d_diffuse_color IS NULL
					THEN NULL
					ELSE '#000000'::text
				END AS metallic_roughness,
				sd.x3d_emissive_color AS emmisive_color,
				NULL AS diffuse_color,
				sd.x3d_specular_color AS specular_glossiness
			FROM feature ftr
			LEFT JOIN geometry_data gd ON gd.feature_id = ftr.id
			LEFT JOIN surface_data_mapping sdm ON sdm.geometry_data_id = gd.id
			LEFT JOIN surface_data sd ON sd.id = sdm.surface_data_id
			WHERE sdm.texture_mapping IS NULL
			  AND sdm.world_to_texture_mapping IS NULL
			  AND sdm.georeferenced_texture_mapping IS NULL
			 ) AS krn1
			 GROUP BY krn1.objectid
			--kernel ended here
		 ) as mtf_ea, dflt
		 ) as mtf_all;