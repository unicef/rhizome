
DROP TABLE IF EXISTS region_heirarchy_cache;

CREATE TABLE region_heirarchy_cache
(
	region_id INTEGER NOT NULL
	, contained_by INTEGER NOT NULL
);

SELECT 
	r.id
	,r.parent_region_id
FROM region r
WHERE EXISTS (
	SELECT 1 from region cntry
	WHERE r.parent_region_id = cntry.id
	AND cntry.parent_region_id is null
)





-- CREATE TABLE region_heirarchy_cache
-- AS
-- WITH RECURSIVE region_heirarchy AS (
--   (	
--   
-- 	SELECT 
-- 		  0 as lvl -- COUNTRIES
-- 		, r.id as region_id
-- 		, r.region_type_id
-- 		, r.parent_region_id
-- 	FROM region r
-- 	WHERE r.parent_region_id IS NULL
-- 
-- 	UNION ALL
-- 	
-- 	SELECT 
-- 		1 as lvl -- CHILDREN OF COUNTRIES
-- 		, id as region_id
-- 		, region_type_id
-- 		, parent_region_id
-- 	FROM region r
-- 	WHERE EXISTS (
-- 		SELECT 1 from region r_par
-- 		WHERE r.parent_region_id = r_par.id
-- 		AND r_par.parent_region_id IS NULL
-- 	)
-- 	AND r.parent_region_id IS NOT NULL
--   ) 
-- 
--   UNION ALL
-- 
--   SELECT   -- Recursive Term
-- 	  rh_c.lvl + 1 as lvl
-- 	, r.id as region_id
-- 	, r.region_type_id
-- 	, r.parent_region_id
--   FROM region_heirarchy rh, region r
--   WHERE r.parent_region_id = rh.region_id
-- )
-- 
-- SELECT DISTINCT 
-- 	ROW_NUMBER() OVER (ORDER by region_id) as id
-- 	,lvl
-- 	,region_id
-- 	,region_type_id
-- 	,parent_region_id
-- 	,x.something_else
-- FROM
-- (SELECT DISTINCT * FROM region_heirarchy) x;
-- 
-- ALTER TABLE region_heirarchy_cache ADD PRIMARY KEY (region_id);
-- GRANT SELECT on region_heirarchy_cache to djangoapp;

