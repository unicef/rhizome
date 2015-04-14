DROP FUNCTION IF EXISTS fn_build_region_tree(cache_job_id INT);
CREATE FUNCTION fn_build_region_tree(cache_job_id INT)
RETURNS TABLE(
	parent_region_id INT
	,lvl INT
) AS
$func$
BEGIN
	-- FIRST CREATE THE TEMP TABLE HOLDING
		-- INITIALLY THE STORED DATA --

	EXECUTE FORMAT ('

	DROP TABLE IF EXISTS _tmp_agg_data;
	CREATE TABLE _tmp_agg_data AS

	SELECT
		d.id
		,d.region_id
		,d.campaign_id
		,d.indicator_id
		,d.value
		,d.cache_job_id
	FROM datapoint d
	WHERE d.cache_job_id = %1$s;',$1);

	--

	RETURN QUERY

    WITH RECURSIVE reg_tree AS
    (

  	SELECT DISTINCT
  		r.id as region_id
		,d.indicator_id
		,d.campaign_id
  		,r.parent_region_id
  		,r.region_type_id
  		,0 as lvl
  		,3 as cache_job_id
  	FROM region r
  	INNER JOIN _tmp_agg_data d
  	ON r.id = d.region_id

  	UNION ALL

    	-- recursive term --
    SELECT DISTINCT
  		r.id as region_id
		,rtr.indicator_id
		,rtr.campaign_id
  		,r.parent_region_id
  		,r.region_type_id
  		,rtr.lvl + 1 as lvl
  		,rtr.cache_job_id
  	FROM reg_tree AS rtr
  	INNER JOIN region r
  	ON rtr.parent_region_id = r.id
  	AND rtr.region_id != r.id
  	AND rtr.region_type_id != r.region_type_id -- This breaks with Kirachi.
  	AND rtr.lvl < 5 -- should not need this. but would be very hard to debug otherwise
  	)
  	SELECT DISTINCT d.parent_region_id,d.lvl
  	FROM reg_tree d
	WHERE d.parent_region_id is not null
  	ORDER BY d.lvl DESC;

END
$func$ LANGUAGE PLPGSQL;

--SELECT * FROM fn_build_region_tree(3)
