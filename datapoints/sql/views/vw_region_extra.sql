
DROP VIEW IF EXISTS vw_region_extra;
CREATE VIEW vw_region_extra as

SELECT
id
,name
,parent_region_id
,is_high_risk
,region_type_id
FROM region;

GRANT SELECT ON vw_region_extra TO djangoapp;
