
DROP TABLE IF EXISTS _odk_settlements;
CREATE TABLE _odk_settlements AS
SELECT ovs.*
FROM (
	SELECT
		settlementcode
		,MAX(created_at) as created_at
		,MAX(submissiondate) as submissiondate
	FROM odk_vcm_settlement
	GROUP BY settlementcode
)x
INNER JOIN odk_vcm_settlement ovs
ON x.settlementcode = ovs.settlementcode
AND x.submissiondate = ovs.submissiondate
AND x.created_at = ovs.created_at;


-- DEAL WITH DUPE NAMES --

UPDATE _odk_settlements ods
SET settlementname = z.full_name
FROM (
	SELECT
		settlementcode
		, settlementname || ' (' || sr.source_guid || ')' as full_name
	-- 	, settlementname
	-- 	,sr.source_guid as parent_name
	FROM (
		SELECT outr.settlementname,settlementcode
		FROM (
			SELECT
				settlementname
				,COUNT(1)
			 FROM _odk_settlements ovs
			 GROUP BY settlementname HAVING COUNT(1) > 1
		)x
		INNER JOIN _odk_settlements outr
		ON x.settlementname = outr.settlementname
	)y
	INNER JOIN source_region sr
	ON sr.region_code = LEFT(y.settlementcode,4)
)z
WHERE z.settlementcode = ods.settlementcode;

-- DELETE ACTUAL DUPES.. IE NOT REGIONS WITH SAME NAME WITH DIFF PARENT--
DELETE
FROM _odk_settlements
WHERE settlementname in
(
	SELECT
		settlementname
		--,count(*) AS C
	FROM _odk_settlements
	GROUP BY settlementname having count(*) > 1
);

DELETE
FROM _odk_settlements
WHERE REPLACE(settlementname,' ' ,'-') in
(
	SELECT
		REPLACE(settlementname,' ' ,'-')
		--,count(*) AS C
	FROM _odk_settlements
	GROUP BY REPLACE(settlementname,' ' ,'-') having count(*) > 1
);


-- CREATE NEW SOURCE REGOINS --
INSERT INTO source_region
(source_guid, lat,lon, document_id, region_code, parent_name, parent_code, region_type, country, is_high_risk)

SELECT settlementname, settlementgps_latitude, settlementgps_longitude,1000,settlementcode,left(settlementcode,4),left(settlementcode,4),'settlement','Nigeria', 't'
FROM _odk_settlements ovs
WHERE NOT EXISTS (
	SELECT 1 FROM source_region sr
	WHERE ovs.settlementcode = sr.region_code
);

-- UPDATE LON/LAT ON SOURCE REGIONS THAT EXISTS --

UPDATE source_region
SET lat = settlementgps_latitude
	,lon = settlementgps_longitude
	,source_guid = ovs.settlementname
FROM _odk_settlements ovs
WHERE region_code = ovs.settlementcode;


-- UPDATE LON/LAT ON MASTER REGIONS THAT EXISTS --

UPDATE region
SET latitude = CAST(settlementgps_latitude AS FLOAT)
	,longitude = CAST(settlementgps_longitude AS FLOAT)
FROM _odk_settlements ovs
WHERE region_code = ovs.settlementcode;

-- CREATE NEW MASTER REGIONS --

INSERT INTO region
(parent_region_id, name, region_code, latitude, longitude, region_type_id, office_id, slug,created_at,source_id,is_high_risk)

SELECT
 	 pr.id as parent_region_id
 	,ovs.settlementname
 	,ovs.settlementcode as region_code
 	,CAST(ovs.settlementgps_latitude AS FLOAT)
 	,CAST(ovs.settlementgps_longitude AS FLOAT)
 	,2 as region_type_id --settlement
 	,1 as office_id -- nigeria
 	,REPLACE(settlementname,' ' ,'-') as region_slug
 	,now()
 	,s.id
 	,CAST(0 as BOOLEAN)
FROM _odk_settlements ovs
INNER JOIN source_region sr
	ON ovs.settlementcode = sr.region_code
INNER JOIN region pr
	ON LEFT(CAST(ovs.settlementcode AS VARCHAR), 4) = pr.region_code
INNER JOIN source s
	ON 1=1
	AND s.source_name = 'odk'
WHERE NOT EXISTS (
	SELECT 1 FROM region r
	where sr.region_code = r.region_code
)
AND NOT EXISTS (
	SELECT 1 FROM region r2
	where ovs.settlementname = r2.name
)
AND NOT EXISTS (
	SELECT 1 FROM region r3
	WHERE REPLACE(settlementname,' ' ,'-') = r3.slug
);


-- CREATE NEW MAPS -- 
