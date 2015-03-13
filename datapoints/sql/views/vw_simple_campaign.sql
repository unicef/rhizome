
DROP VIEW IF EXISTS vw_simple_campaign;
CREATE VIEW vw_simple_campaign as


SELECT

	ROW_NUMBER()
 	,c.office_id
	,c.start_date
	,c.id as campaign_id
	,c.end_date
	,c.slug
	,da.region_id
FROM campaign c
INNER JOIN datapoint_abstracted da
ON c.id = da.campaign_id;


GRANT SELECT ON vw_simple_campaign TO djangoapp;
