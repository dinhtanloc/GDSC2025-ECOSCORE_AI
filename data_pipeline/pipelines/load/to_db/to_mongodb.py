from pymongo import MongoClient
from configs.settings import MONGO_URI

def push_to_mongo(company_code, text, gcs_path):
    client = MongoClient(MONGO_URI)
    db = client.stock_pipeline
    doc = {
        "company_code": company_code,
        "full_text": text,
        "file_url": gcs_path,
    }
    db.documents.insert_one(doc)
    print("✅ Data pushed to MongoDB")