
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


UPDATE source_datapoint as sr
set region_string = x.new_str
FROM
(
SELECT DISTINCT
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
REPLACE(region_string,'2014',''),
'2013',''),'2012',''),'January',''),'February',''),'March',''),'April',''),'May',''),'June',''),'July',''),'August',''),'September',''),'October',''),'November',''),'December',''),'   - ',' - ') as new_str
,region_string
FROM source_datapoint 
)x
WHERE x.region_string = sr.region_string


INSERT INTO region_type (name)
SELECT 'Country' WHERE NOT EXISTS ( SELECT 1 from region_type where name = 'Country' ) UNION ALL  
SELECT 'Province'WHERE NOT EXISTS ( SELECT 1 from region_type where name = 'Province' )   UNION ALL  
SELECT 'District' WHERE NOT EXISTS ( SELECT 1 from region_type where name = 'District' )  UNION ALL  
SELECT 'Ward' WHERE NOT EXISTS ( SELECT 1 from region_type where name = 'Ward' )  UNION ALL  
SELECT 'Settlement' WHERE NOT EXISTS ( SELECT 1 from region_type where name = 'Settlement' ) 

-------------------------------------------
-------------------------------------------
-- NOW AUTO INSERTING FROM REGION UPLOAD --
-------------------------------------------
-------------------------------------------

----------------------
-- INSERT COUNTRIES --
----------------------



INSERT INTO region
(office_id,latitude,longitude,slug,source_id,region_code,is_high_risk,name,source_region_id,region_type_id,created_at)

SELECT 
	o.id
	,CAST( sr.lat as FLOAT )
	,CAST(sr.lon as FLOAT)
	,LOWER(replace(sr.region_string,' ','-')) as slug
	,2 -- region upload
	,sr.region_code
	,sr.is_high_risk
	,sr.region_string
	,sr.id
	,rt.id
	,now()
FROM source_region sr
INNER JOIN office o 
ON sr.country = o.name
INNER JOIN region_type rt
on sr.region_type = rt.name
WHERE sr.region_type = 'Country'
AND NOT EXISTS 
(
	SELECT 1 FROM region r
	where sr.region_string = r.name
	and r.office_id = o.id
	and r.region_type_id = rt.id 
);

--- NEED TO TAKE OUT THE REGIONAL ENTITES FROM HEIRARCHY ---

update source_region sr
set parent_name = gg.parent_name
from  source_region gg
where gg.region_type =  'Region'
and sr.parent_name =  gg.region_string

-------------------------
--- INSERT PROVINCES --
-------------------------
INSERT INTO region
(parent_region_id,office_id,latitude,longitude,slug,source_id,region_code,is_high_risk,name,source_region_id,region_type_id,created_at)

SELECT 
	pr.id as parent_region_id
	,o.id
	,CAST( sr.lat as FLOAT )
	,CAST(sr.lon as FLOAT)
	,LOWER(replace(sr.region_string,' ','-')) as slug
	,2 -- region upload
	,sr.region_code
	,sr.is_high_risk
	,sr.region_string
	,sr.id
	,rt.id
	,now()
FROM source_region sr
INNER JOIN office o 
ON LOWER(sr.country) = lower(o.name)
INNER JOIN region_type rt
ON sr.region_type = rt.name
INNER JOIN region pr
ON sr.parent_name = pr.name
WHERE sr.region_type = 'Province'
AND NOT EXISTS 
(
	SELECT 1 FROM region r
	where sr.region_string = r.name
	and r.office_id = o.id
	and r.region_type_id = rt.id 
);


-----------------------------
--- FCT SHOULD BE FCT, ABUJA 
-----------------------------
update source_region
set region_string = 'FCT, Abuja'
where region_string = 'FCT'

update region
set name = 'FCT, Abuja'
where name = 'FCT'


---------------------------------------------
-- append (LGA) to duplicative district names
---------------------------------------------
update source_region ser 
set region_string = ser.region_string || ' ' || x.rt 
from 
(
	SELECT 'Afghanistan' as c, '(District)' as rt UNION ALL
	SELECT 'Nigeria', '(LGA)'
) x
where ser.country = x.c
and region_type = 'District'
and exists 
(
	select 1 from region r
	where r.name = ser.region_string 
)

--------------------
-- FIX "Musakhel" --
--------------------
update source_region
set region_string = region_string || ' (' || parent_name || ')'
where region_string = 'Musakhel'


-----------------------------
--- INSERT DISTRICTS (1336)--
-----------------------------
 

INSERT INTO region
(parent_region_id,office_id,latitude,longitude,slug,source_id,region_code,is_high_risk,name,source_region_id,region_type_id,created_at)

SELECT 
	pr.id as parent_region_id
	,o.id
	,CAST( sr.lat as FLOAT )
	,CAST(sr.lon as FLOAT)
	,LOWER(replace(sr.region_string,' ','-')) as slug
	,2 -- region upload
	,sr.region_code
	,sr.is_high_risk
	,sr.region_string
	,sr.id
	,rt.id
	,now()
FROM source_region sr
INNER JOIN office o 
ON LOWER(sr.country) = lower(o.name)
INNER JOIN region_type rt
ON sr.region_type = rt.name
INNER JOIN region pr
ON sr.parent_name = pr.name
WHERE sr.region_type = 'District'
AND NOT EXISTS 
(
	SELECT 1 FROM region r
	where sr.region_string = r.name
	and r.office_id = o.id
	and r.region_type_id = rt.id 
);

select count(*) from source_region
select count(*) from region

------------------
-- ADD MAPPINGS --
------------------

insert into region_map
(master_region_id,source_region_id,mapped_by_id)
select id,r.source_region_id,1
from region r
where not exists
(
	select 1 from region_map rm
	where r.source_region_id = rm.source_region_id

)

------------------------------------------------------
---- NOW I NEED TO ALTER THE NAMES OF THE REGIONS ----
----- FOR WHICH EXISTS LGAS WITH THE SAME NAME -------
------------------------------------------------------


update region r
set name = x.stripped_name || ' (Province)'
from
(
	select id,name,replace(name,' (District)','') as stripped_name From region where name like '%(District)%'
)x
where x.stripped_name = r.name

update region 
set slug = slug || '-province'
where name like '% (Province)%';


update source_region sr
set region_string = r.name
from region r
where sr.id = r.source_region_id
and r.name like '%(Province%';


update source_region sr
set region_string = r.name
from region r
where sr.id = r.source_region_id
and r.name like '%(District%';




-----------------------------------------------
-- Bring Back Indicators ( along w source )  --
-----------------------------------------------

-----------------------------------------------
-- Bring Back campaigns ( along w office )  --
-----------------------------------------------


----------------------------------------------------
-- NOW BRING BACK THE DATAPOINTS BY  --
----------------------------------------------------




