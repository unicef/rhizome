DROP FUNCTION IF EXISTS fn_prep_agg_datapoint(cache_job_id INT);
CREATE FUNCTION fn_prep_agg_datapoint(cache_job_id INT)
RETURNS TABLE(
	--region_id int
	parent_region_id int
	--,region_type_id int
	,lvl int
	--,cache_job_id int
) AS $$

    WITH RECURSIVE reg_tree AS
    (

  	SELECT DISTINCT
  		r.id as region_id
  		,r.parent_region_id
  		,r.region_type_id
  		,0 as lvl
  		,3 as cache_job_id
  	FROM region r
  	INNER JOIN datapoint d
  	ON r.id = d.region_id
  	AND d.cache_job_id = $1

  	UNION ALL

    	-- recursive term --
    	SELECT DISTINCT
  		r.id as region_id
  		,r.parent_region_id
  		,r.region_type_id
  		,lvl + 1 as lvl
  		,$1 as cache_job_id
  	FROM reg_tree AS rtr
  	INNER JOIN region r
  	ON rtr.parent_region_id = r.id
  	AND rtr.region_id != r.id
  	AND rtr.region_type_id != r.region_type_id -- This breaks with Kirachi.
  	AND lvl < 5 -- should not need this. but would be very hard to debug otherwise
  	)

  	SELECT DISTINCT parent_region_id,lvl
  	FROM reg_tree d
  	ORDER BY lvl DESC;



$$

LANGUAGE SQL;


SELECT * FROM fn_prep_agg_datapoint(1)
