DROP FUNCTION IF EXISTS fn_test_data_accuracy();
CREATE FUNCTION fn_test_data_accuracy() 
RETURNS TABLE(id int, region_id INT ,campaign_id INT,indicator_id INT ,target_value FLOAT ,actual_value FLOAT)

    AS $$ 

    UPDATE recon_data rd
    SET success_flag = tr.success_flag
    FROM (
	SELECT
		rd.id
		,rd.region_id
		,rd.campaign_id
		,rd.indicator_id
		,rd.target_value
		,dwc.value as actual_value
		,CAST(CASE WHEN ( ABS(rd.target_value - dwc.value) < 0.001) THEN 1 ELSE 0 END AS BOOLEAN) as success_flag
	    FROM recon_data rd
	    LEFT JOIN datapoint_with_computed dwc
	    ON rd.region_id = dwc.region_id
	    AND rd.campaign_id = dwc.campaign_id
	    AND rd.indicator_id = dwc.indicator_id) tr 
    WHERE rd.id = tr.id;

    SELECT
    	rd.id,rd.region_id,rd.campaign_id,rd.indicator_id,rd.target_value,dwc.value as actual_value
    FROM recon_data rd
    LEFT JOIN datapoint_with_computed dwc
	    ON rd.region_id = dwc.region_id
	    AND rd.campaign_id = dwc.campaign_id
	    AND rd.indicator_id = dwc.indicator_id
    WHERE success_flag = 'f'
 
    $$
    LANGUAGE SQL;

