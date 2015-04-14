DROP FUNCTION IF EXISTS fn_agg_datapoint(cache_job_id INT,region_ids int[]);
CREATE FUNCTION fn_agg_datapoint(cache_job_id INT,region_ids int[] )
RETURNS TABLE(id int) AS
	$func$
	BEGIN

		--
		PERFORM * FROM fn_agg_prep($1);

		RETURN QUERY

		SELECT ad.id FROM agg_datapoint ad
		--WHERE dwc.cache_job_id = $1
		LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
