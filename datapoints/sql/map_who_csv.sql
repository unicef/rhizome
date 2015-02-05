DROP TABLE IF EXISTS _tmp_who_regions;

CREATE TEMP TABLE _tmp_who_regions AS
SELECT sr.id as source_region_id, sr.region_string, rt.id as region_type_id, rt.name as region_type, sr.document_id
FROM source_region sr
INNER JOIN (
  SELECT 871 as doc_id, 'sub-district' as region_type UNION ALL
  SELECT 875  ,'sub-district'  UNION ALL
  SELECT 855  ,'district' UNION ALL
  SELECT 887, 'settlement'
)x
ON sr.document_id = x.doc_id
INNER JOIN region_type rt
on x.region_type = rt.name
WHERE document_id in ( 855,871,875,887 )
AND NOT EXISTS (
  SELECT 1 FROM region_map rm
  WHERE sr.id = rm.source_region_id
);

DELETE FROM _tmp_who_regions WHERE source_region_id IN (
  SELECT twr.source_region_id
  FROM _tmp_who_regions twr
  INNER JOIN
  (
    SELECT region_string,region_type_id,min(source_region_id) as keep_this_id
    FROM _tmp_who_regions
    GROUP BY region_string,region_type_id
  )x
  ON x.region_string = twr.region_string
  AND x.region_type_id = twr.region_type_id
  AND twr.source_region_id != keep_this_id
);

DROP TABLE IF EXISTS _parenth_names;
CREATE TEMP TABLE _parenth_names
AS

SELECT
  rc.name as child_full_name
  ,rp.name as parent_name
  ,REPLACE(rc.name  ,'(' || rp.name || ')','') as stripped_child_name
FROM region rc
INNER JOIN region rp
ON rc.parent_region_id = rp.id
AND rp.name like '%(' || rc.name||'%'

SELECT * FROM _parenth_names;

INSERT INTO region_map
(source_region_id, master_region_id, mapped_by_id)

DELETE FROM _tmp_who_regions
WHERE source_region_id in (
SELECT
  twr.source_region_id
-- 	, r.id as master_region_id
-- 	, 1 as mapped_by_id
FROM _tmp_who_regions twr
INNER JOIN region r
ON r.name like '%' || twr.region_string || ' (%'
AND twr.region_type_id = r.region_type_id
GROUP BY twr.source_region_id having count(*) > 1

INSERT INTO region_map
(source_region_id, master_region_id, mapped_by_id)
SELECT
  twr.source_region_id
   , r.id as master_region_id
   , 1 as mapped_by_id
FROM _tmp_who_regions twr
INNER JOIN region r
ON r.name like '%' || twr.region_string || ' (%'
AND twr.region_type_id = r.region_type_id
