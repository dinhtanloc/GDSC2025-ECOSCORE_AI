from sqlalchemy import create_engine

class PostgresLoader:
    def __init__(self, db_config):
        self.engine = create_engine(
            f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )

    def load_dataframe(self, df, table_name, schema='public', if_exists='replace'):
        df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
        df.to_sql(table_name, con=self.engine, index=False, if_exists=if_exists, schema=schema)
        print(f"✅ Saved to PostgreSQL: {table_name}")