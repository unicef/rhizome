
-- Create sourceID for John SQL --

DROP TABLE IF EXISTS _ng_setts;
CREATE TABLE _ng_setts AS

SELECT
sr.id
,sr.region_code as region_slug
,sr.region_string || ' (' || sr.parent_name || ')' as region_string
,sr.region_type
,sr.region_code
,r.id as parent_region_id
,sr.parent_name
,country
,sr.is_high_risk
,sr.parent_code
FROM source_region sr
LEFT JOIN region r
ON sr.parent_code = r.region_code
WHERE sr.document_id = 917;

SELECT distinct parent_code FROM _ng_setts
WHERE parent_region_id is null


INSERT INTO region
(office_id,slug,source_id,region_code,is_high_risk,name,parent_region_id,region_type_id,created_at)
-- -- --
SELECT
	o.id
	,region_slug
	,s.id
	,ngs.region_code
	,is_high_risk
	,region_string
	,parent_region_id
	,rt.id
	,now()
FROM _ng_setts ngs
INNER JOIN office o
ON ngs.country = o.name
INNER JOIN source s
on s.source_name = 'John_SQL'
INNER JOIN region_type rt
ON LOWER(ngs.region_type) = LOWER(rt.name)
WHERE NOT EXISTS (
	SELECT 1 FROM region r
	WHERE ngs.region_string = r.name
)
AND NOT EXISTS (
	SELECT 1 FROM region r2
	WHERE ngs.region_code = r2.region_code
)


INSERT INTO region_map
(master_id,source_id,mapped_by_id)
SELECT
	r.id as master_id
	,ngs.id as source_id
	,1
FROM _ng_setts ngs
INNER JOIN region r
ON ngs.region_code = r.region_code
WHERE NOT EXISTS (
	SELECT 1 from region_map rm
	WHERE ngs.id = rm.source_id
);
