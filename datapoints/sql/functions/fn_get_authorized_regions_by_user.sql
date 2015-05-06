DROP FUNCTION IF EXISTS fn_get_authorized_regions_by_user(cache_job_id int);
CREATE FUNCTION fn_get_authorized_regions_by_user(cache_job_id int)
RETURNS TABLE(id int) AS
$func$
BEGIN

	RETURN QUERY

	SELECT r.id FROM region r
	--WHERE dwc.cache_job_id = $1
	LIMIT 1;

END
$func$ LANGUAGE PLPGSQL;
