DROP FUNCTION IF EXISTS fn_get_authorized_regions_by_user(user_id int, list_of_region_ids integer[]);
DROP FUNCTION IF EXISTS fn_get_authorized_regions_by_user(user_id int, list_of_region_ids integer[], read_write varchar(1));
CREATE FUNCTION fn_get_authorized_regions_by_user(user_id int, list_of_region_ids integer[], read_write varchar(1))

RETURNS TABLE(

  id INT
  ,parent_region_id INT
  ,office_id INT
  ,region_type_id INT
  ,name VARCHAR
) AS
$func$
BEGIN

	RETURN QUERY

	WITH RECURSIVE region_tree AS
	(
	-- non-recursive term ( rows where the components aren't
	-- master_indicators in another calculation )

	SELECT
		rg.parent_region_id
		,rg.parent_region_id as immediate_parent_id
		,rg.id as region_id
		,0 as lvl
	FROM region rg

	UNION ALL

	-- recursive term --
	SELECT
		r_recurs.parent_region_id
		,rt.parent_region_id as immediate_parent_id
		,rt.region_id
		,rt.lvl + 1
	FROM region AS r_recurs
	INNER JOIN region_tree AS rt
	ON (r_recurs.id = rt.parent_region_id)
	AND r_recurs.parent_region_id IS NOT NULL
	)

	SELECT
		r.id
		,r.parent_region_id
		,r.office_id
		,r.region_type_id
		,r.name
	FROM region_tree rt
	INNER JOIN region r
	ON rt.region_id = r.id
	WHERE EXISTS (
		SELECT 1
		FROM region_permission rm
		WHERE rm.user_id = $1
		AND rt.parent_region_id = rm.region_id
		AND rm.read_write = $3
	)
  AND r.id = ANY(COALESCE($2,ARRAY[r.id]))

  UNION ALL

  SELECT
    r.id
    ,r.parent_region_id
    ,r.office_id
    ,r.region_type_id
    ,r.name
  FROM region r
  INNER JOIN region_permission rp
    ON r.id = rp.region_id
    AND rp.user_id = $1
    AND r.id = ANY(COALESCE($2,ARRAY[r.id]))
    AND rp.read_write = $3;

END
$func$ LANGUAGE PLPGSQL;
