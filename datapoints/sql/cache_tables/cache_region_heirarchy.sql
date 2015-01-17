
DROP TABLE IF EXISTS _tmp_heirarchy;

CREATE TEMP TABLE _tmp_heirarchy  
AS

SELECT r.id as region_id, r.region_type_id, r.parent_region_id as  contained_by 
FROM region r
INNER JOIN region country
ON r.parent_region_id = country.id
and country.parent_region_id is null;

--Insert my direct parent AND insert the "contained by" as a separate record
INSERT INTO _tmp_heirarchy
(region_id,region_type_id,contained_by)

SELECT 
	x.region_id
	, x.region_type_id
	, contained_by
FROM ( 	-- only 2 lvls so dont need to be recursive... yet --
	SELECT 
		r.id as region_id
		, r.region_type_id
		,r.parent_region_id as contained_by
	FROM region r 
	INNER JOIN _tmp_heirarchy rhc
	ON r.parent_region_id = rhc.region_id

	UNION ALL 

	SELECT 
		r.id as region_id
		, r.region_type_id
		, rhc.contained_by
	FROM region r 
	INNER JOIN _tmp_heirarchy rhc
	ON r.parent_region_id = rhc.region_id
)x
WHERE NOT EXISTS ( 
	SELECT 1 FROM _tmp_heirarchy rhc
	WHERE rhc.region_id = x.region_id
);

-- Populate the Cache
DROP TABLE IF EXISTS region_heirarchy_cache;
CREATE TABLE region_heirarchy_cache
AS 
SELECT  
	row_number() OVER (ORDER BY x.region_id,x.contained_by) as id
	,x.*
FROM ( SELECT DISTINCT * FROM _tmp_heirarchy ) x ; 

-- grant select, create clustered ix --
GRANT SELECT ON region_heirarchy_cache to djangoapp;
CREATE INDEX rt_pr_ix ON region_heirarchy_cache ( contained_by, region_type_id) ;
CLUSTER region_heirarchy_cache USING rt_pr_ix;