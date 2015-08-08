DROP FUNCTION IF EXISTS fn_get_source_dps_to_sync(user_id INT, document_id INT, input_indicator_id INT);
DROP FUNCTION IF EXISTS fn_upsert_source_dps(user_id INT, document_id INT, input_indicator_id INT);
CREATE FUNCTION fn_upsert_source_dps(user_id INT, document_id INT, input_indicator_id INT)
RETURNS TABLE
(
	 id INT
) AS
$func$
BEGIN

		DROP TABLE IF EXISTS _to_sync;
		CREATE TEMP TABLE _to_sync AS

    SELECT
          sd.id as source_datapoint_id
        , CAST(sd.cell_value AS FLOAT) as value
        , rm.master_object_id as region_id
        , cm.master_object_id as campaign_id
        , im.master_object_id as indicator_id
    FROM source_datapoint sd
    INNER JOIN source_region sr
			ON sd.region_code = sr.region_code
			AND sd.document_id =  $2
    INNER JOIN region_map rm
      ON sr.id = rm.source_object_id
    INNER JOIN source_indicator si
      ON sd.indicator_string = si.indicator_string
    INNER JOIN indicator_map im
      ON si.id = im.source_object_id
      AND im.master_object_id = COALESCE($3,im.master_object_id)
    INNER JOIN source_campaign sc
      ON sd.campaign_string = sc.campaign_string
    INNER JOIN campaign_map cm
      ON sc.id = cm.source_object_id;

	 --IF THERE ARE DUPES DO NOT INSERT THEM --
	 -- FIXME: this requires a screen and workflow for reviewing conflicting data

	 DELETE FROM _to_sync ts_out
	 USING (
	    SELECT
		 	    ts.region_id, ts.campaign_id, ts.indicator_id
		  FROM _to_sync ts
			GROUP BY ts.region_id, ts.campaign_id, ts.indicator_id HAVING COUNT(1) > 1
	 ) x
	 WHERE ts_out.region_id = x.region_id
	 AND ts_out.indicator_id = x.indicator_id
	 AND ts_out.indicator_id = x.indicator_id;


		INSERT INTO datapoint
		(campaign_id, changed_by_id, indicator_id, region_id, source_datapoint_id, value, created_at, cache_job_id)

		SELECT
			  ts.campaign_id
			, $1 as changed_by_id
			, ts.indicator_id
			, ts.region_id
			, ts.source_datapoint_id
			, ts.value
			, now() as created_at
			, -1 as cache_job_id

		FROM _to_sync ts
		WHERE NOT EXISTS (
			SELECT 1 FROM datapoint d
			where ts.region_id = d.region_id
			AND ts.indicator_id = d.indicator_id
			AND ts.campaign_id = d.campaign_id
		);

		UPDATE datapoint
			SET value = ts.value
				, changed_by_id = $1
				, created_at = NOW()
				, source_datapoint_id = ts.source_datapoint_id
		FROM _to_sync ts
		WHERE datapoint.region_id = ts.region_id
		AND datapoint.campaign_id = ts.campaign_id
		AND datapoint.indicator_id = ts.indicator_id;

		RETURN QUERY

		SELECT d.id
		FROM source_datapoint sd
		INNER JOIN datapoint d
		ON sd.id = d.source_datapoint_id
		AND sd.document_id = $2;


END
$func$ LANGUAGE PLPGSQL;
