import requests
import pandas as pd
from db_utils import get_connection
from psycopg2.extras import execute_values

# Function for inserting values into RDS
def insert_forex_rates(rates_df: pd.DataFrame):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO forex_rates (date, base_currency, target_currency, rate)
                    VALUES %s
                    ON CONFLICT (date, base_currency, target_currency) DO NOTHING;
                """
                values = list(rates_df.itertuples(index=False, name=None))
                execute_values(cur, insert_query, values)
            conn.commit()
        print(f"Inserted {len(values)} rows successfully.")
    except Exception as db_err:
        print(f"Database error: {db_err}")

url = "https://api.frankfurter.dev/v2/rates"

query_params = {
    'base': 'USD',
    'quotes': 'BND,KHR,IDR,LAK,MYR,MMK,PHP,SGD,THB,VND',
    'from': '2025-08-07',
    'to': '2026-08-06'
}

records = []

# Extract phase
try:
    response = requests.get(url, params=query_params)
    response.raise_for_status()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error: {http_err}")
    exit()
except requests.exceptions.RequestException as req_err:
    print(f"Request failed: {req_err}")
    exit()

# Parse JSON
try:
    forex = response.json()
except ValueError:
    print('Failed to parse JSON.')
    exit()

# Validate API response
if not forex:
    print('API returned no data.')
    exit()

# Transform phase
for row in forex:
    record = {'date': row.get('date'),
              'base_currency': row.get('base'),
              'target_currency': row.get('quote'),
              'rate': row.get('rate')}

    if None not in record.values():
        records.append(record)

if not records:
    print('No records returned.')
else:
    df = pd.DataFrame(records)
    df = df.drop_duplicates()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df.dropna().reset_index(drop=True)

    print(f"Prepared {len(df)} records for insertion.")
    insert_forex_rates(df)


