import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
GCS_BUCKET_NAME = "your-bucket"
BIGQUERY_PROJECT = "your-project"
BIGQUERY_DATASET = "your_dataset"
POSTGRES_URL = "postgresql+psycopg2://user:pass@host/db"
MONGO_URI = "mongodb://localhost:27017/"
