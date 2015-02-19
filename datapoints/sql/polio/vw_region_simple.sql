
DROP VIEW IF EXISTS vw_simple_region;
CREATE VIEW vw_simple_region as

SELECT
r.id
,r.name
,parent_region_id
FROM region r
INNER JOIN region_type rt
ON r.region_type_id = rt.id
AND parent_region_id is NULL;

GRANT SELECT ON vw_simple_region TO djangoapp;
