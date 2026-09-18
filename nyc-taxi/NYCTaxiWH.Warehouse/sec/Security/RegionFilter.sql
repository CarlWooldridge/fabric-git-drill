CREATE SECURITY POLICY [sec].[RegionFilter]
    ADD FILTER PREDICATE [sec].[fn_region_predicate]([region]) ON [dbo].[emp_demo]
    WITH (STATE = ON);


GO