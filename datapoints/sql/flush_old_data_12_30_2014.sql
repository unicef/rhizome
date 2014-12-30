
-- -- delete all datapoints --
-- 
-- SELECT d.*
-- --delete 
-- FROM datapoint d
-- WHERE region_id in 
-- (
-- 	select r.id from region r 
-- 	inner join office o 
-- 	on r.office_id = o.id
-- 	and o.name = 'Afghanistan'
-- )


-- remove all mappings --
--truncate table region_map;
--truncate table campaign_map;
--truncate table indicator_map;

--truncate table source_campaign cascade;

select * from source_datapoint sd
inner join datapoint d
on sd.id = d.source_datapoint_id
inner join source_data_document doc
on sd.document_id = doc.id
and doc.docfile = 'documents/2014/12/30/AFG_MASTER_MgmtIndicators_20141229_v0.1.csv'


-- burbaba
select * from region 
where name = 'Maywand'


select * from datapoint where region_id in (
select r.id from region r
inner join office o 
on r.office_id = o.id
and o.name = 'Nigeria')


select sd.id,im.master_indicator_id,rm.master_region_id,cm.master_campaign_id
select distinct r


select * from source_region limit 10


select * from source_datapoint sd
where document_id = 851
and not exists 
(
	select 1 from datapoint d
	where sd.id = d.source_datapoint_id
)




select * 
from source_datapoint sd
inner join source_indicator si
on si.indicator_string = sd.indicator_string
inner join indicator_map im
on si.id = im.source_indicator_id
and sd.document_id = 851
inner join source_region sr 
on sd.region_string = sr.region_string
inner join region_map rm 
on sr.id = rm.source_region_id
inner join source_campaign sc 
on sd.campaign_string = sc.campaign_string
inner join campaign_map cm 
on sc.id = cm.source_campaign_id
and not exists 
(
	select 1 from datapoint d
	where sd.id = d.source_datapoint_id
)
and not exists 
(
	select 1 from datapoint d2
	where cm.master_campaign_id = d2.campaign_id
	and rm.master_region_id = d2.region_id
	and im.master_indicator_id = d2.indicator_id
)


select * from datapoint 
where indicator_id = 34
and region_id = 12910
and campaign_id = 116



select * 



