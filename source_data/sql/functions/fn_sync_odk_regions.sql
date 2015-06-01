
DROP TABLE IF EXISTS _odk_regions;
CREATE TABLE _odk_regions AS
SELECT
	odk_vcm.*
	, sr.id as source_region_id
	, CAST(NULL AS INT) AS master_region_id
FROM odk_vcm_settlement odk_vcm
LEFT JOIN region sr
ON odk_vcm.settlementcode = sr.region_code;

DROP TABLE IF EXISTS _source_odk_setts;
CREATE TABLE _source_odk_setts AS
SELECT
	sr.id as source_region_id
	, sr.region_code
	, sr.parent_code
	, r.id as region_id
	, r.region_code as cleaned_code
FROM source_region sr
LEFT JOIN region r
ON r.slug = sr.parent_code
WHERE sr.country = 'Nigeria'
AND region_type = 'Settlement'

SELECT * FROM _source_odk_setts sos
INNER JOIN



-- TRY TO MAP TO EXISTING SOURCE REGIONS BY UN-HACKING REGION CODE --

-- INSERT NEW SOURCE REGIONS --

-- UPDATE EXISTING SOURCE REGIONS WITH INFORMATION FROM NEW --

-- FOR THOSE JUST INSERTED / UPDATED .. UPDATE PRODUCTION
  --> CREATE NEW MASTER REGIONS FOR THOSE THAT DON"T EXISTS
  --> CREATE MAP RECORDS FOR UNMAPPED
