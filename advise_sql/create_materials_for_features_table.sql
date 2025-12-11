-- Table: citydb._materials_for_features

-- DROP TABLE IF EXISTS citydb._materials_for_features;

CREATE TABLE IF NOT EXISTS citydb._materials_for_features
(
    id SERIAL NOT NULL,
    namespace_of_classname text,
    classname text,
    namespace_of_property text,
    property_name text,
    column_name_of_property_value text,
    property_value text,
    emmisive_color text,
    pbr_metallic_roughness_base_color text,
    pbr_metallic_roughness_metallic_roughness text,
    pbr_specular_glossiness_diffuse_color text,
    pbr_specular_glossiness_specular_glossiness text,
    CONSTRAINT _materials_for_features_v1_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS citydb._materials_for_features
    OWNER to tester;