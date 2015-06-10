DROP FUNCTION IF EXISTS fn_get_source_dbs_to_sync(user_id INT, document_id INT, input_indicator_id INT);
DROP FUNCTION IF EXISTS fn_get_source_dps_to_sync(user_id INT, document_id INT, input_indicator_id INT);
CREATE FUNCTION fn_get_source_dps_to_sync(user_id INT, document_id INT, input_indicator_id INT)
RETURNS TABLE
(
	 id INT
	,cell_value VARCHAR(255)
	,region_id INT
	,campaign_id INT
	,indicator_id INT
) AS
$func$
BEGIN

		DROP TABLE IF EXISTS _tmp_permissions;
		CREATE TEMP TABLE _tmp_permissions AS
		SELECT
			  x.region_id
			, y.indicator_id
		FROM (
			SELECT
				spr.id as region_id
			FROM fn_get_authorized_regions_by_user($1 , NULL, 'w',NULL) spr
		)x
		INNER JOIN (
			SELECT ip.indicator_id
			FROM indicator_permission ip
			INNER JOIN auth_user_groups aug
			ON ip.group_id = aug.group_id
			AND aug.user_id = $1
		) y
		ON 1=1;


  	RETURN QUERY

    SELECT
          sd.id
        , CAST(sd.cell_value AS VARCHAR)
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
      ON sc.id = cm.source_object_id
		WHERE EXISTS (
			SELECT 1 FROM _tmp_permissions tp
			WHERE tp.region_id = rm.master_object_id
			AND tp.indicator_id = im.master_object_id
		);

END
$func$ LANGUAGE PLPGSQL;
