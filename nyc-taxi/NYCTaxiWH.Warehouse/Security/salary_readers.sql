CREATE ROLE [salary_readers]
    AUTHORIZATION [dbo];


GO

ALTER ROLE [salary_readers] ADD MEMBER [test.north@carlwooldridgeicloud.onmicrosoft.com];


GO

ALTER ROLE [salary_readers] ADD MEMBER [carl@carlwooldridgeicloud.onmicrosoft.com];


GO