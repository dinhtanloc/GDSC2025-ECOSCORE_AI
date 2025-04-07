import pandas as pd
from sqlalchemy import create_engine
from configs.settings import POSTGRES_URL

def push_to_postgres(company_code, text):
    engine = create_engine(POSTGRES_URL)
    df = pd.DataFrame([{ "company_code": company_code, "text_summary": text[:500] }])
    df.to_sql("financial_reports", engine, if_exists="append", index=False)
    print("✅ Data pushed to PostgreSQL")