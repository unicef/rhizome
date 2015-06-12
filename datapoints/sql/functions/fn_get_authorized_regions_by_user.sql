DROP FUNCTION IF EXISTS fn_get_authorized_regions_by_user(user_id int, list_of_region_ids integer[], read_write varchar(1),depth_level INT);
CREATE FUNCTION fn_get_authorized_regions_by_user(user_id int, list_of_region_ids integer[], read_write varchar(1),depth_level INT)

RETURNS TABLE(

   lvl INT
  ,id INT
  ,office_id INT
  ,name VARCHAR
  ,parent_region_id INT
  ,region_type_id INT
  ,has_children BOOLEAN
) AS
$func$
BEGIN


  DROP TABLE IF EXISTS _permitted_regions;

	CREATE TABLE _permitted_regions AS
	WITH RECURSIVE region_tree(parent_region_id, immediate_parent_id, region_id, lvl) AS
  	(
  	-- non-recursive term ( rows where the components aren't
  	-- master_indicators in another calculation )

  	SELECT
  		rg.parent_region_id
  		,rg.parent_region_id as immediate_parent_id
  		,rg.id as region_id
  		,1 as lvl
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

  	SELECT * FROM (

  		SELECT rt.lvl,r.*
  		FROM region_tree rt
  		INNER JOIN region r
  		ON rt.region_id = r.id
  		WHERE EXISTS (
  			SELECT 1
  			FROM region_permission rm
  			WHERE rm.user_id = $1
  			AND rm.read_write = $3
  			AND rt.parent_region_id = rm.region_id
  		)

  		UNION ALL
  		SELECT
  			0 as lvl
  			,r.*
  		FROM region r
  		INNER JOIN region_permission rp
  		ON r.id = rp.region_id
  		AND rp.user_id = $1
  		AND rp.read_write = $3

  	)x
  	WHERE x.id = ANY(COALESCE($2,ARRAY[x.id]));

    DROP TABLE IF EXISTS _has_parent;
    CREATE TABLE _has_parent AS

    SELECT
        prm.id
        ,CASE WHEN x.parent_region_id IS NULL THEN 0 ELSE 1 END as has_children
    FROM _permitted_regions prm
    LEFT JOIN (
      SELECT DISTINCT r.parent_region_id FROM region r
    )x
    ON prm.id = x.parent_region_id;


	  RETURN QUERY

  	SELECT
      prm.lvl
     ,prm.id
     ,prm.office_id
     ,prm.name
     ,prm.parent_region_id
     ,prm.region_type_id
     ,CAST(hp.has_children AS BOOLEAN)
  	FROM _permitted_regions prm
    INNER JOIN _has_parent hp
    ON prm.id = hp.id
    WHERE prm.lvl <= COALESCE($4,prm.lvl)

  	ORDER BY prm.lvl;

END
$func$ LANGUAGE PLPGSQL;
