DROP FUNCTION IF EXISTS fn_agg_prep(cache_job_id INT);
CREATE FUNCTION fn_agg_prep(cache_job_id INT)

RETURNS TABLE(
	parent_region_id INT
	,lvl INT
) AS
$func$
BEGIN
	-- FIRST CREATE THE TEMP TABLE HOLDING
		-- INITIALLY THE STORED DATA --

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
	WHERE d.cache_job_id = $1;

	--
	DROP TABLE IF EXISTS _reg_tree;
	CREATE TABLE _reg_tree AS

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
  	AND rtr.lvl < 5 -- should not need this. but would be very hard to debug if this condition was satisfied.
  	)

  	SELECT DISTINCT d.parent_region_id,d.lvl
  	FROM reg_tree d
	WHERE d.parent_region_id is not null
  	ORDER BY d.lvl DESC;

	INSERT INTO _tmp_agg_data
	(id,region_id, campaign_id, indicator_id, value, cache_job_id)
	SELECT
		d.id, d.region_id, d.campaign_id, d.indicator_id, value, $1

	FROM _reg_tree rt
 	INNER JOIN region rp
 		ON rt.parent_region_id = rp.parent_region_id
	INNER JOIN datapoint d
		ON d.region_id = rp.id
	WHERE EXISTS (
		SELECT 1 FROM _tmp_agg_data tad
		WHERE tad.campaign_id = d.campaign_id
		AND tad.indicator_id = d.indicator_id
	)
	AND NOT EXISTS (
		SELECT 1 FROM _tmp_agg_data tad
		WHERE d.id = tad.id
	);

	RETURN QUERY

	SELECT * FROM _reg_tree ORDER BY lvl ASC;

-- 	;

END
$func$ LANGUAGE PLPGSQL;

-- SELECT COUNT(*) FROM _tmp_agg_data
--
-- SELECT * FROM fn_build_region_tree(3)
