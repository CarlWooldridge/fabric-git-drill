CREATE TABLE [dbo].[emp_demo] (
    [emp_id]    INT                                                  NOT NULL,
    [emp_name]  VARCHAR (50)                                         NOT NULL,
    [region]    VARCHAR (20)                                         NOT NULL,
    [email]     VARCHAR (100) MASKED WITH (FUNCTION = 'email()')     NULL,
    [salary]    DECIMAL (10, 2) MASKED WITH (FUNCTION = 'default()') NULL,
    [owner_upn] VARCHAR (100)                                        NOT NULL
);


GO