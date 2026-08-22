CREATE TABLE silver.forex_rates (
    "date" date NOT NULL,
    base_currency varchar(3) NOT NULL,
    target_currency varchar(3) NOT NULL,
    rate numeric(20, 8) NOT NULL,
    ingestion_timestamp timestamp NOT NULL,
    CONSTRAINT uq_forex_rates UNIQUE (date, base_currency, target_currency)
);