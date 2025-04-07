from google.cloud import bigquery
import pandas as pd
from configs.settings import BIGQUERY_PROJECT, BIGQUERY_DATASET, BIGQUERY_TABLE

def save_metadata(company_code, gcs_path, text):
    client = bigquery.Client(project=BIGQUERY_PROJECT)
    table_id = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"

    df = pd.DataFrame([{
        "company_code": company_code,
        "gcs_path": gcs_path,
        "text": text,
    }])

    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print("✅ Metadata pushed to BigQuery")