DROP FUNCTION IF EXISTS fn_get_authorized_regions_by_user(user_id int);
CREATE FUNCTION fn_get_authorized_regions_by_user(user_id int)
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


	SELECT
		r.id
		,r.parent_region_id
		,r.office_id
		,r.region_type_id
		,r.name
	FROM region r
	WHERE EXISTS (
		SELECT 1
		FROM region_permission rm
		WHERE rm.user_id = 1
		AND r.id = rm.region_id
	);



END
$func$ LANGUAGE PLPGSQL;
