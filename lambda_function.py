import requests
import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):

    URL = "https://api.frankfurter.dev/v2/rates"

    query_params = {
        'base': 'USD',
        'quotes': 'BND,KHR,IDR,LAK,MYR,MMK,PHP,SGD,THB,VND',
    }

    try:
        response = requests.get(URL, params=query_params)
        print(f'API Status Code: {response.status_code} - {response.reason}')
        response.raise_for_status()

        records = response.json()

        now = datetime.now()
        ingestion_date = now.strftime("%Y-%m-%d")
        for record in records:
            record['ingestion_date'] = ingestion_date

        json_records = "\n".join(json.dumps(record) for record in records)

        print(json_records)

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise

    try:
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        s3 = boto3.client('s3')
        bucket = os.environ['S3_BUCKET_NAME']

        key = f"records/year={year}/month={month}/day={day}/asean_rates.json"

        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json_records,
            ContentType='application/x-ndjson',
            Metadata={
                'source': 'Frankfurter-API',
            }
        )

        print(f"Uploaded {key} to {bucket}")

        glue = boto3.client('glue')
        crawler_name = os.environ['GLUE_CRAWLER_NAME']
        glue.start_crawler(Name=crawler_name)
        print(f'Glue crawler "{crawler_name}" started. S3 will now be crawled for new data.')
    except Exception as e:
        print(f"S3 error: {e}")
        raise
