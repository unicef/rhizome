
-- UPDATE REGION CODE FOR ALL SOURCE POLYGONS --

UPDATE source_region
SET region_code = 'shape-' || region_code
WHERE id in  (
	SELECT source_id from source_region_polygon
);


-- DUPE REGION MAPS --

DROP TABLE IF EXISTS dupe_sr;
CREATE TEMP TABLE dupe_sr AS
SELECT
	MAX(rm.id) as max_region_map_id
	, region_code
	, COUNT(1) AS C
	, CAST(NULL AS INT) AS has_map_conflict
FROM source_region sr
INNER JOIN region_map rm
ON sr.id = rm.source_id
GROUP BY region_code HAVING COUNT(1) > 1;

--
DELETE FROM region_map
USING source_region sr
INNER JOIN dupe_sr dsr
ON sr.region_code = dsr.region_code
AND id != dsr.max_region_map_id
WHERE source_id = sr.id;


DELETE
FROM source_region_polygon srp
WHERE NOT EXISTS (
	SELECT 1 FROM region_map rm
	WHERE srp.source_id = rm.source_id
);


DELETE
FROM source_region sr
WHERE NOT EXISTS (
	SELECT 1 FROM region_map rm
	WHERE sr.id = rm.source_id
);



--SELECT *
DELETE
FROM source_campaign sc
WHERE NOT EXISTS (
	SELECT 1 FROM campaign_map cm
	WHERE sc.id = cm.source_id
);


--SELECT *
DELETE
FROM source_indicator si
WHERE NOT EXISTS (
	SELECT 1 FROM indicator_map im
	WHERE si.id = im.source_id
);

--SELECT COUNT(*)
DELETE
FROM source_datapoint sd
WHERE NOT EXISTS (
	SELECT 1 FROM datapoint d
	WHERE sd.id = d.source_datapoint_id
);

-- DUPE SOURCE REGION --

DELETE
FROM source_region sr
USING (
	SELECT
		MAX(sr.id) as max_region_id
		, region_code
		, COUNT(1) AS C
	FROM source_region sr
	GROUP BY region_code HAVING COUNT(1) > 1
)x
WHERE sr.region_code = x.region_code
AND sr.id != x.max_region_id;

DELETE FROM region_map
WHERE source_id in (
	SELECT id from source_region
	WHERE region_code is null
);

DELETE FROM source_region
WHERE region_code is null;
