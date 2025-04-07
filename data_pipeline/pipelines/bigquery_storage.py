from google.cloud import storage
import os

def upload_file_to_gcs(local_path, bucket_name, gcs_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Uploaded {local_path} → gs://{bucket_name}/{gcs_path}")

# Example
upload_file_to_gcs("data/VNM_report_2024.pdf", "your-bucket", "raw/2024/VNM_report_2024.pdf")
