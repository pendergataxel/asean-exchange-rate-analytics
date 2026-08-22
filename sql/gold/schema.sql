CREATE TABLE gold.dim_country_currency (
    currency_code varchar(3) NOT NULL,
    currency_name varchar(50) NOT NULL,
    country_name varchar(50) NOT NULL,
    country_code varchar(3) NOT NULL,
    sea_subregion varchar(20) NOT NULL,

    CONSTRAINT dim_country_currency_pkey
        PRIMARY KEY (currency_code),

    CONSTRAINT dim_country_currency_sea_subregion_check
        CHECK (sea_subregion IN ('Mainland', 'Maritime'))
);


CREATE TABLE gold.dim_date (
    "date" date NOT NULL,
    "day" int2 NOT NULL,
    day_name varchar(10) NOT NULL,
    day_of_week int2 NOT NULL,
    week_of_year int2 NOT NULL,
    "month" int2 NOT NULL,
    month_name varchar(10) NOT NULL,
    quarter int2 NOT NULL,
    "year" int2 NOT NULL,
    year_month varchar(7) NOT NULL,
    is_weekend bool NOT NULL,
    is_month_end bool NOT NULL,
    is_quarter_end bool NOT NULL,

    CONSTRAINT dim_date_pkey
        PRIMARY KEY (date)
);


CREATE TABLE gold.fact_forex_rates (
    "date" date NOT NULL,
    currency_code varchar(3) NOT NULL,
    rate numeric(20, 10) NOT NULL,
    ingestion_timestamp timestamp NOT NULL,

    CONSTRAINT fact_forex_rates_pkey
        PRIMARY KEY (date, currency_code)
);


ALTER TABLE gold.fact_forex_rates
ADD CONSTRAINT fact_forex_rates_currency_code_fkey
FOREIGN KEY (currency_code)
REFERENCES gold.dim_country_currency(currency_code);


ALTER TABLE gold.fact_forex_rates
ADD CONSTRAINT fact_forex_rates_date_fkey
FOREIGN KEY ("date")
REFERENCES gold.dim_date("date");