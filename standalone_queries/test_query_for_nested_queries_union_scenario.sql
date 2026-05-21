SELECT
	shll.krnl_id as id,
	shll.feature_id,
	shll.prnt_name as pro_name,
	json_objectagg(CONCAT(shll.alias, '_', shll.name) : shll.pro_value) as pro_value
FROM
(
SELECT 
	pro.id,
	pro.name,
	ns.alias,
	krnl.id as krnl_id,
	krnl.feature_id,
	CONCAT(krnl.alias, '_', krnl.name) as prnt_name,
	CASE
		WHEN pro.datatype_id = 2 THEN pro.val_int::text
		WHEN pro.datatype_id = 3 THEN pro.val_int::text
		WHEN pro.datatype_id = 4 THEN pro.val_double::text
		WHEN pro.datatype_id = 5 THEN pro.val_string::text
		WHEN pro.datatype_id = 6 THEN pro.val_uri::text
		WHEN pro.datatype_id = 7 THEN pro.val_timestamp::text
		WHEN pro.datatype_id = 14 THEN pro.val_string::text
		WHEN pro.datatype_id = 17 THEN pro.val_double::text
		WHEN pro.datatype_id = 701 THEN pro.val_array::text
		WHEN pro.datatype_id = 702 THEN 'none'::text
	END AS pro_value
FROM property AS pro
LEFT JOIN namespace AS ns ON 
	ns.id = pro.namespace_id
LEFT JOIN (
	SELECT pro_krnl.id,
            pro_krnl.name,
			pro_krnl.feature_id,
            ns_krnl.alias
     FROM property AS pro_krnl
     LEFT JOIN namespace AS ns_krnl ON ns_krnl.id = pro_krnl.namespace_id
     WHERE pro_krnl.parent_id IS NULL
	 AND pro_krnl.datatype_id IN (2,3,4,5,6,7,14,17,701,702) 
) AS krnl ON
	krnl.id = pro.parent_id
WHERE pro.datatype_id IN (2,3,4,5,6,7,14,17,701,702)
	AND pro.parent_id IS NOT NULL
) AS shll
GROUP BY shll.krnl_id, shll.prnt_name, shll.feature_id
UNION ALL
SELECT 
	pro.id,
	pro.feature_id,
	CONCAT(ns.alias, '_', pro.name) AS pro_name,
	to_json(CASE
		WHEN pro.datatype_id = 2 THEN pro.val_int::text
		WHEN pro.datatype_id = 3 THEN pro.val_int::text
		WHEN pro.datatype_id = 4 THEN pro.val_double::text
		WHEN pro.datatype_id = 5 THEN pro.val_string::text
		WHEN pro.datatype_id = 6 THEN pro.val_uri::text
		WHEN pro.datatype_id = 7 THEN pro.val_timestamp::text
		WHEN pro.datatype_id = 14 THEN pro.val_string::text
		WHEN pro.datatype_id = 17 THEN pro.val_double::text
		WHEN pro.datatype_id = 701 THEN pro.val_array::text
		WHEN pro.datatype_id = 702 THEN 'none'::text
	END) AS pro_value
FROM property AS pro
LEFT JOIN namespace AS ns ON 
	ns.id = pro.namespace_id
WHERE pro.datatype_id IN (2,3,4,5,6,7,14,17,701,702)
	AND pro.parent_id IS NULL