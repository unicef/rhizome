DROP FUNCTION IF EXISTS fn_find_bad_data(cache_job_id INT);
CREATE FUNCTION fn_find_bad_data(cache_job_id INT)
RETURNS TABLE(id int, error_type varchar, doc_id int) AS $$

	DELETE FROM bad_data 
	WHERE cache_job_id = $1;

	INSERT INTO bad_data
	(datapoint_id,error_type,document_id,cache_job_id)
	
        SELECT x.id, x.error_type, sd.document_id as doc_id, $1
        FROM (
            SELECT id, 'negative_value' as error_type, source_datapoint_id
            FROM datapoint d
	    WHERE cache_job_id = $1
            AND value < 0.00

            UNION ALL

            SELECT d.id, 'campaign_wrong_country', source_datapoint_id
            FROM datapoint d
            INNER JOIN region r
                ON d.region_id = r.id
            INNER JOIN campaign c
                ON d.campaign_id = c.id
            WHERE r.office_id != c.office_id
            AND cache_job_id = $1
        )x

        INNER JOIN source_datapoint sd
            ON x.source_datapoint_id = sd.id;

		
$$

LANGUAGE SQL;


SELECT * FROM fn_find_bad_data(-1)
