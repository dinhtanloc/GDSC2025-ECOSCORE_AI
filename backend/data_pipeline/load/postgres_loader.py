from sqlalchemy import create_engine

class PostgresLoader:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)

    def load_dataframe(self, df, table_name, schema='public', if_exists='replace'):
        df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
        df.to_sql(table_name, con=self.engine, index=False, if_exists=if_exists, schema=schema)
        print(f"✅ Saved to PostgreSQL: {table_name}")