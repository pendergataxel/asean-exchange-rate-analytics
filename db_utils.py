import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv('ASEAN_ANALYTICS_ENDPOINT'),
        port=os.getenv('ASEAN_ANALYTICS_PORT'),
        database=os.getenv('ASEAN_ANALYTICS_NAME'),
        user=os.getenv('ASEAN_ANALYTICS_USER'),
        password=os.getenv('ASEAN_ANALYTICS_PASS')
    )

