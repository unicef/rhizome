
-- Create sourceID for John SQL --

INSERT INTO source(source_name,source_description)
SELECT 'John_SQL', 'John SQL'
WHERE NOT EXISTS ( 
	SELECt 1 from SOURCE where source_name = 'John_SQL'
);

DROP TABLE IF EXISTS _ng_setts;
CREATE TABLE _ng_setts AS

SELECT
   sr.id
  ,LOWER(REPLACE(REPLACE(sr.region_string,' ','-'),'/','-')) as region_slug
  ,sr.region_string
  ,sr.region_type
  ,sr.region_code
  ,r.id as parent_region_id
  ,sr.parent_name
  ,country
  ,sr.is_high_risk
FROM source_region sr
LEFT JOIN region r
ON sr.parent_name = r.name
WHERE sr.document_id in (869,874);

UPDATE _ng_setts
SET region_type = 'sub-district'
WHERE region_type = 'Ward';

UPDATE _ng_setts
SET region_type = 'settlement'
WHERE region_type = 'Settlement';


-- deal with dupes in the existsing dataset --
DROP TABLE IF EXISTS _dupe_names;
CREATE TEMP TABLE _dupe_names AS

SELECT
	ngs.region_string
	,ngs.region_string || ' (' || region_type || ')' || ' (' || country || ')' as new_string
	,ngs.parent_name
	,ngs.region_type
FROM (
SELECT
	region_string
	,count(*) AS C
FROM _ng_setts
GROUP BY region_string HAVING count(*) > 1
)x
INNER JOIN _ng_setts ngs
on ngs.region_string = x.region_string;


UPDATE _ng_setts ngs
set region_string = new_string
FROM _dupe_names dn
WHERE dn.region_string = ngs.region_string;


-- If region has multiple names append parent name
DROP TABLE IF EXISTS _dupe_names;
CREATE TEMP TABLE _dupe_names AS
SELECT 
	ngs.region_string
	,ngs.region_string || ' (' || region_type || ')' || ' (' || country || ')' as new_string
FROM _ng_setts ngs
INNER JOIN office o 
ON ngs.country = o.name
WHERE EXISTS ( 
	SELECT 1 from region r 
	WHERE r.name = ngs.region_string
	AND r.office_id != o.id
);

UPDATE _ng_setts ngs
set region_string = new_string
FROM _dupe_names dn
WHERE dn.region_string = ngs.region_string;

INSERT INTO region 
(office_id,slug,source_id,region_code,is_high_risk,name,parent_region_id,source_region_id,region_type_id,created_at)

SELECT 
	o.id
	,region_slug
	,s.id
	,ngs.region_code
	,is_high_risk
	,region_string
	,parent_region_id
	,ngs.id
	,rt.id
	,now()
FROM _ng_setts ngs
INNER JOIN office o 
ON ngs.country = o.name
INNER JOIN source s
on s.source_name = 'John_SQL'
INNER JOIN region_type rt
ON ngs.region_type = rt.name
WHERE NOT EXISTS ( 
	SELECT 1 FROM region r
	WHERE ngs.region_string = r.name
)
AND NOT EXISTS ( 
	SELECT 1 FROM region r2
	WHERE ngs.region_code = r2.region_code
)
AND NOT EXISTS ( 
	SELECT 1 FROM region r2
	WHERE ngs.region_code = r2.region_code
)
AND ngs.parent_region_id is NOT NULL;

INSERT INTO region_map 
(master_region_id,source_region_id,mapped_by_id)
SELECT 
	r.id as master_region_id
	,ngs.id as source_region_id
	,1
FROM _ng_setts ngs
INNER JOIN region r
ON ngs.id = r.source_region_id
WHERE NOT EXISTS ( 
	SELECT 1 from region_map rm
	WHERE ngs.id = rm.source_region_id
-- 	AND r.id = rm.master_region_id
);


