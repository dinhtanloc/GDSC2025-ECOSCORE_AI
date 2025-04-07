from pipelines.load.to_gcs import upload_to_gcs
from pipelines.load.to_bigquery import save_metadata
from pipelines.process.text_embedding import extract_text_from_pdf
from pipelines.load.to_db.to_postgres import push_to_postgres
from pipelines.load.to_db.to_mongodb import push_to_mongo

def main():
    local_file = "data/raw/VNM_report_2024.pdf"
    company = "VNM"

    gcs_path = upload_to_gcs(local_file, company)
    text = extract_text_from_pdf(local_file)

    save_metadata(company, gcs_path, text)
    push_to_postgres(company, text)
    push_to_mongo(company, text, gcs_path)

if __name__ == "__main__":
    main()