SELECT *
FROM dbo.emp_demo




SELECT HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'CONTROL') AS has_control,
       IS_ROLEMEMBER('db_owner')                          AS is_db_owner;