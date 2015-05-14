--SELECT * FROM fn_populate_doc_meta(1013)
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

	DROP TABLE IF EXISTS _tmp_indicator_permissions;
	CREATE TEMP TABLE _tmp_indicator_permissions AS

	SELECT DISTINCT ip.indicator_id
	FROM auth_user_groups aug
	INNER JOIN indicator_permission ip
		ON aug.user_id = $1
		AND aug.group_id = ip.group_id
		AND ip.indicator_id = COALESCE(CAST($3 AS INT),ip.indicator_id);

	DROP TABLE IF EXISTS _tmp_region_permissions;
	CREATE TEMP TABLE _tmp_region_permissions AS

	WITH RECURSIVE region_tree AS
	(
	-- non-recursive term ( rows where the components aren't
	-- master_indicators in another calculation )

	SELECT
		COALESCE(rg.parent_region_id, rg.id) as parent_region_id
		,rg.parent_region_id as immediate_parent_id
		,rg.id as region_id
		,0 as lvl
	FROM region rg

	UNION ALL

	-- recursive term --
	SELECT
		r_recurs.parent_region_id
		,rt.parent_region_id as immediate_parent_id
		,rt.region_id
		,rt.lvl + 1
	FROM region AS r_recurs
	INNER JOIN region_tree AS rt
	ON (r_recurs.id = rt.parent_region_id)
	AND r_recurs.parent_region_id IS NOT NULL
	)

	SELECT rt.region_id FROM region_tree rt
	INNER JOIN region_permission rm
	ON rt.parent_region_id = rm.region_id
	AND rm.user_id = 1
	AND rm.read_write = 'w';


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
      ON sc.id = cm.source_object_id
    WHERE EXISTS (
	SELECT 1 FROM _tmp_indicator_permissions tip
	WHERE im.master_object_id = tip.indicator_id
    )
     AND EXISTS (
 	SELECT 1 FROM _tmp_region_permissions trp
 	WHERE rm.master_object_id = trp.region_id
     );

END
$func$ LANGUAGE PLPGSQL;
