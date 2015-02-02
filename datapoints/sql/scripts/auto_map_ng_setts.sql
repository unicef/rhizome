

DROP TABLE IF EXISTS _ng_setts;

CREATE TABLE _ng_setts AS

SELECT
  sr.region_string
--   ,sr.region_ype
  ,sr.region_code
  ,r.id as parent_region_id
  ,sr.parent_name
 

FROM source_region sr
LEFT JOIN region r
ON sr.parent_name = r.name
WHERE sr.document_id = 874;


SELECT distinct parent_name,parent_region_id  FROM _ng_setts
WHERE parent_region_id is not null