CREATE TABLE [gold].[fact_trips] (
    [vendorID]             INT            NULL,
    [PickupDatetime]       DATETIME2 (6)  NULL,
    [DropoffDatetime]      DATETIME2 (6)  NULL,
    [PickupDate]           DATE           NULL,
    [DropoffDate]          DATE           NULL,
    [Duration]             BIGINT         NULL,
    [passengerCount]       INT            NULL,
    [tripDistance]         FLOAT (53)     NULL,
    [puLocationId]         INT            NULL,
    [doLocationId]         INT            NULL,
    [pickupLongitude]      FLOAT (53)     NULL,
    [pickupLatitude]       FLOAT (53)     NULL,
    [dropoffLongitude]     FLOAT (53)     NULL,
    [dropoffLatitude]      FLOAT (53)     NULL,
    [rateCodeID]           INT            NULL,
    [storeAndFwdFlag]      VARCHAR (8000) NULL,
    [paymentType]          INT            NULL,
    [fareAmount]           FLOAT (53)     NULL,
    [extra]                FLOAT (53)     NULL,
    [mtaTax]               FLOAT (53)     NULL,
    [improvementSurcharge] VARCHAR (8000) NULL,
    [tipAmount]            FLOAT (53)     NULL,
    [tollsAmount]          FLOAT (53)     NULL,
    [ehailFee]             FLOAT (53)     NULL,
    [totalAmount]          FLOAT (53)     NULL,
    [tripType]             INT            NULL
);


GO