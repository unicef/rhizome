DROP FUNCTION IF EXISTS fn_get_source_dbs_to_sync(user_id INT, document_id INT, input_indicator_id INT);
CREATE FUNCTION fn_get_source_dbs_to_sync(user_id INT, document_id INT, input_indicator_id INT)
RETURNS TABLE
(
	 id INT
	,vell_value VARCHAR(255)
	,region_id INT
	,campaign_id INT
	,indicator_id INT
) AS
$func$
BEGIN

	DROP TABLE IF EXISTS _tmp_permissions;
	CREATE TEMP TABLE _tmp_permissions AS
	SELECT * FROM region_permission  rm
	WHERE rm.user_id = $1;

  	RETURN QUERY

    SELECT
          sd.id
        , sd.cell_value
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

END
$func$ LANGUAGE PLPGSQL;
