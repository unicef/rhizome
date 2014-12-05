DROP VIEW IF EXISTS parent_region_agg;
CREATE VIEW parent_region_agg
AS

select 
	row_number() OVER (ORDER BY cntry.id,indicator_id,campaign_id) AS id
	,cntry.id as parent_region_id
	,d.indicator_id
	,d.campaign_id
	,sum(coalesce(d.value, 0)) as the_sum

from office o 
inner join region cntry
on o.name = cntry.name
inner join region r2
on r2.office_id = o.id
inner join datapoint d
on r2.id = d.region_id
group by cntry.id,d.campaign_id,d.indicator_id







