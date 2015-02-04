
DROP VIEW IF EXISTS vw_simple_region;
CREATE VIEW vw_simple_region as

SELECT
id
,name
,parent_region_id
FROM region;

GRANT SELECT ON vw_simple_region TO djangoapp;
