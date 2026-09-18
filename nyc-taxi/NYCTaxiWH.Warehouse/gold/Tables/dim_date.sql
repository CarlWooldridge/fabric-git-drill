CREATE TABLE [gold].[dim_date] (
    [Datetime]  DATETIME2 (6)  NULL,
    [Date]      DATE           NULL,
    [Year]      INT            NULL,
    [Month]     INT            NULL,
    [Quarter]   INT            NULL,
    [MonthName] VARCHAR (8000) NULL,
    [DayName]   VARCHAR (8000) NULL,
    [holiday]   VARCHAR (8000) NULL
);


GO