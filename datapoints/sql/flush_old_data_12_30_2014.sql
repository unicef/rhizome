


-- delete all datapoints --

select d.*
delete 
from datapoint d
where region_id in (

select r.id from region r 
inner join office o 
on r.office_id = o.id
and o.name = 'Afghanistan'
)


-- remove all mappings --
truncate table region_map;
truncate table campaign_map;
truncate table indicator_map;

--https://www.youtube.com/watch?v=cUfIKX5ReKQ


