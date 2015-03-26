DROP FUNCTION IF EXISTS fn_find_bad_data(cache_job_id INT);
CREATE FUNCTION fn_find_bad_data(cache_job_id INT)
RETURNS TABLE(id int) AS $$

	
	SELECT DISTINCT ID
	FROM datapoint limit 1
		
$$

LANGUAGE SQL;


