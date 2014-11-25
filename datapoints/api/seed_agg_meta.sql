
DROP TABLE IF EXISTS tmp;
TRUNCATE TABLE aggregation_expected_data cascade;
TRUNCATE TABLE aggregation_type cascade;


CREATE TEMP TABLE tmp AS
select *,'calc_pct_solo_region_solo_campaign' as agg_type 
from 
(
SELECT 'region_solo' as slug ,'region' as content_type,'solo' as param_type UNION ALL
SELECT  'campaign_solo','campaign','solo' UNION ALL
SELECT  'indicator_part','indicator','part' UNION ALL
SELECT  'indicator_whole','indicator','whole'
)x

UNION ALL

SELECT *, 'calc_pct_parent_region_solo_campaign' as agg_type
from 
(
SELECT 'region_parent' as slug ,'region' as content_type, 'parent'as param_type UNION ALL
SELECT 'indicator_whole','indicator','whole' UNION ALL
SELECT 'campaign_solo','campaign','solo' UNION ALL
SELECT 'indicator_part' ,'indicator','part'
) x;


INSERT INTO aggregation_type
(name,slug,display_name_w_sub,created_at)
SELECT DISTINCT agg_type, agg_type, agg_type, now() 
FROM tmp;

INSERT INTO aggregation_expected_data
(aggregation_type_id, content_type, param_type, slug, created_at)
SELECT at.id,t.content_type, t.param_type, t.slug,now()
FROM tmp t
inner join aggregation_type at
on t.agg_type = at.slug;


select * from aggregation_expected_data

