DROP FUNCTION IF EXISTS fn_calc_datapoint(cache_job_id int);
CREATE FUNCTION fn_calc_datapoint(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

	--
	PERFORM * FROM fn_calc_prep($1);
	--
	PERFORM * FROM fn_calc_sum_of_parts($1);
	-- -- --
  PERFORM * FROM fn_calc_part_over_whole($1);
	-- -- --
	PERFORM * FROM fn_calc_part_of_difference($1);
	--
	PERFORM * FROM fn_calc_upsert_computed($1);

	-- FIX ME --
	DELETE FROM datapoint_with_computed dwc
	WHERE location_id is null;

	RETURN QUERY

	SELECT dwc.id FROM datapoint_with_computed dwc
	WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
