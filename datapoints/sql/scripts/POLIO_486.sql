
DROP TABLE IF EXISTS _bad_campaign_datapoints;
CREATE TEMP TABLE _bad_campaign_datapoints AS

SELECT 
	  d.id as datapoint_id
        , changed_by_id
	, r.id as region_id
	, r.name
	, r.office_id as region_office_id
	, c.office_id as campaign_office_id
	, source_datapoint_id
	, value
	, c.slug
    , d.created_at
FROM datapoint d
INNER JOIN region r 
	ON d.region_id = r.id
INNER JOIN campaign c 
	ON d.campaign_id = c.id	
AND c.office_id != r.office_id;

-- Data Entry Things --
DELETE FROM datapoint WHERE id IN (
	SELECT datapoint_id from _bad_campaign_datapoints bdc
	WHERE bdc.source_datapoint_id = -1
);

-- Source Data Things --
DELETE FROM datapoint WHERE id IN (
	SELECT datapoint_id from _bad_campaign_datapoints bdc
);

