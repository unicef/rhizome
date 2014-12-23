
-- creating a document to attribute the new source datapoints to --

insert into source_data_document
(created_by_id, guid,doc_text,is_processed)
select 1, 'initialinsertfromoldmasterdb','initialinsertfromoldmasterdb','t'
WHERE NOT EXISTS 
(
	select 1 from source_data_document 
	where guid = 'initialinsertfromoldmasterdb'
	
);

-- This is inserting the current master datapoints into the source datapoints table -- 
INSERT INTO source_data_sourcedatapoint
(region_string,campaign_string,indicator_string,cell_value,row_number,source_id,document_id,source_guid,status_id,guid,created_at)

SELECT 
	c.name || ' - ' || r.name as region_string
	,c.name as campaign_string
	,i.name as indicator_string
	,d.value
	,d.id as row_number
	,4 as source_id -- datapoint_upload
	,doc.id as document_id
	,c.name || ' - ' || r.name || ' - ' || i.name as source_guid
	,1 as status_id
	,'orig_db_id: ' || d.id as guid
	,now() as created_at	
FROM datapoint d
inner join indicator i 
on d.indicator_id = i.id
inner join region r 
on d.region_id = r.id
inner join campaign c 
on d.campaign_id = c.id
inner join source_data_document doc
on doc.guid = 'initialinsertfromoldmasterdb'
where r.id != 128
and not exists 
(

	select 1 from source_data_sourcedatapoint sd
	where sd.document_id = doc.id
	and sd.row_number = d.id
);


TRUNCATE TABLE datapoint CASCADE;
TRUNCATE TABLE region CASCADE;
TRUNCATE TABLE campaign CASCADE;

DELETE FROM 
source_data_sourcedatapoint sd
USING source_data_document d
WHERE sd.document_id = d.id 
AND d.guid != 'initialinsertfromoldmasterdb';

TRUNCATE TABLE source_data_campaignmap CASCADE;
TRUNCATE TABLE source_data_regionmap CASCADE;
TRUNCATE TABLE source_data_indicatormap CASCADE;
TRUNCATE TABLE source_data_sourceindicator CASCADE;
TRUNCATE TABLE source_data_sourcecampaign CASCADE;
TRUNCATE TABLE source_data_sourceregion CASCADE;

delete from source_data_document where guid != 'initialinsertfromoldmasterdb';


insert into region_type (name)
select 'Country' where not exists ( select 1 from region_type where name = 'Country') UNION ALL
select 'Settlement' where not exists ( select 1 from region_type where name = 'Settlement');

insert into campaign_type
(name)
SELECT 'National Immunization Days (NID)' where not exists 
	(select 1 from campaign_type where name = 'National Immunization Days (NID)') UNION ALL
SELECT 'Sub-national Immunization Days (SNID)' where not exists 
	(select 1 from campaign_type where name = 'Sub-national Immunization Days (SNID)') UNION ALL
SELECT 'SIAD' where not exists 
	(select 1 from campaign_type where name = 'SIAD') UNION ALL
SELECT 'Mop-up' where not exists 
	(select 1 from campaign_type where name = 'Mop-up') 




