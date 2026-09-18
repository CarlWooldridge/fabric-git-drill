CREATE TABLE [gold].[dim_paymenttype] (
    [PaymentTypeID]     INT            NULL,
    [PaymentMethod]     VARCHAR (8000) NULL,
    [ElectronicPayment] BIT            NULL,
    [RequiresTipEntry]  BIT            NULL
);


GO