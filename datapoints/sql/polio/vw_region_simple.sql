
DROP VIEW IF EXISTS vw_simple_region;
CREATE VIEW vw_simple_region as

SELECT
r.id
,r.name
,parent_region_id
FROM region r;

GRANT SELECT ON vw_simple_region TO djangoapp;
