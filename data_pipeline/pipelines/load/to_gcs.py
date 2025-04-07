from google.cloud import storage
from configs.settings import GCS_BUCKET_NAME
import os

def upload_to_gcs(local_path, company_code):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    file_name = os.path.basename(local_path)
    gcs_path = f"raw/{company_code}/{file_name}"
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Uploaded to gs://{GCS_BUCKET_NAME}/{gcs_path}")
    return f"gs://{GCS_BUCKET_NAME}/{gcs_path}"