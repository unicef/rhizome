DROP FUNCTION IF EXISTS fn_get_authorized_locations_by_user(user_id int, list_of_location_ids integer[], read_write varchar(1),depth_level INT);
CREATE FUNCTION fn_get_authorized_locations_by_user(user_id int, list_of_location_ids integer[], read_write varchar(1),depth_level INT)

RETURNS TABLE(

   lvl INT
  ,id INT
  ,office_id INT
  ,name VARCHAR
  ,parent_location_id INT
  ,location_type_id INT
  ,has_children BOOLEAN
) AS
$func$
BEGIN


  DROP TABLE IF EXISTS _permitted_locations;

	CREATE TABLE _permitted_locations AS
	WITH RECURSIVE location_tree(parent_location_id, immediate_parent_id, location_id, lvl) AS
  	(
  	-- non-recursive term ( rows where the components aren't
  	-- master_indicators in another calculation )

  	SELECT
  		rg.parent_location_id
  		,rg.parent_location_id as immediate_parent_id
  		,rg.id as location_id
  		,1 as lvl
  	FROM location rg

  	UNION ALL

  	-- recursive term --
  	SELECT
  		r_recurs.parent_location_id
  		,rt.parent_location_id as immediate_parent_id
  		,rt.location_id
  		,rt.lvl + 1
  	FROM location AS r_recurs
  	INNER JOIN location_tree AS rt
  	ON (r_recurs.id = rt.parent_location_id)
  	AND r_recurs.parent_location_id IS NOT NULL
  	)

  	SELECT * FROM (

  		SELECT rt.lvl,r.*
  		FROM location_tree rt
  		INNER JOIN location r
  		ON rt.location_id = r.id
  		WHERE EXISTS (
  			SELECT 1
  			FROM location_permission rm
  			WHERE rm.user_id = $1
  			AND rm.read_write = $3
  			AND rt.parent_location_id = rm.location_id
  		)

  		UNION ALL
  		SELECT
  			0 as lvl
  			,r.*
  		FROM location r
  		INNER JOIN location_permission rp
  		ON r.id = rp.location_id
  		AND rp.user_id = $1
  		AND rp.read_write = $3

  	)x
  	WHERE x.id = ANY(COALESCE($2,ARRAY[x.id]));

    DROP TABLE IF EXISTS _has_parent;
    CREATE TABLE _has_parent AS

    SELECT
        prm.id
        ,CASE WHEN x.parent_location_id IS NULL THEN 0 ELSE 1 END as has_children
    FROM _permitted_locations prm
    LEFT JOIN (
      SELECT DISTINCT r.parent_location_id FROM location r
    )x
    ON prm.id = x.parent_location_id;


	  RETURN QUERY

  	SELECT
      prm.lvl
     ,prm.id
     ,prm.office_id
     ,prm.name
     ,prm.parent_location_id
     ,prm.location_type_id
     ,CAST(hp.has_children AS BOOLEAN)
  	FROM _permitted_locations prm
    INNER JOIN _has_parent hp
    ON prm.id = hp.id
    WHERE prm.lvl <= COALESCE($4,prm.lvl)

  	ORDER BY prm.lvl;

END
$func$ LANGUAGE PLPGSQL;
