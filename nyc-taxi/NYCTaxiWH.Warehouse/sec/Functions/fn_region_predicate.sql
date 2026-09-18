CREATE FUNCTION sec.fn_region_predicate(@region VARCHAR(20))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS is_visible
FROM sec.user_region AS ur
WHERE ur.user_upn = LOWER(USER_NAME())
  AND (ur.region = @region OR ur.region = '*');

GO