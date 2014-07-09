
CREATE DATABASE polio;

CREATE user djangoapp WITH PASSWORD 'w3b@p01i0';
GRANT ALL PRIVILEGES ON DATABASE "polio" to djangoapp

select * from information_schema.tables
where table_schema = 'public'

DROP TABLE datapoint;
DROP TABLE datapoint_indicator;
DROP TABLE region;


select * from datapoint;
select * from datapoint_indicator;
select * from region;

