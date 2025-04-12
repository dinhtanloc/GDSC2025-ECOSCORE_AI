from .extract.stock_exchange import StockCompanyDataCollector
from .extract.news_crawler import BaoChinhPhuScraper
from .extract.social_media import ArticleScraper
from .extract.annual_report import CafefPDFScraper
from .load.postgres_loader import PostgresLoader
from langchain_community.document_loaders import PyPDFLoader
import os
import pandas as pd
from .load.mongo_loader import MongoDBLoader
from backend.config import PROJECT_CFG
from chatbot.model.config.load_tools_config import TOOLS_CFG

class ETLTable:
    def __init__(self, ticket_collection, db_config):
        """
        Khởi tạo ETL pipeline cho dữ liệu dạng bảng.
        :param ticket_collection: Danh sách các mã chứng khoán cần xử lý.
        :param db_config: Cấu hình kết nối PostgreSQL.
        """
        self.ticket_collection = ticket_collection
        self.extractor = StockCompanyDataCollector(ticket_collection)
        self.loader = PostgresLoader(db_config)

    def extract(self):
        """
        Trích xuất dữ liệu từ các nguồn khác nhau.
        :return: Một dictionary chứa các DataFrame được trích xuất.
        """
        print("Extracting table data...")
        extraction_methods = {
            "profile": "get_profile",
            "financial_ratio": "get_financial_ratio",
            "cash_flow": "get_cashflow",
            "balance_sheet": "get_balance_sheet",
            "income_statement": "get_income_statement",
            "events": "get_events",
            "news": "get_news",
            "company_reports": "get_company_reports",
            "officers": "get_officers",
            "affiliates": "get_affiliates",
            "shareholders": "get_shareholders",
            "ratio_summary": "get_ratio_summary",
            "overview": "get_overview",
        }

        extracted_data = {}
        for table_name, method_name in extraction_methods.items():
            try:
                print(f"Extracting {table_name}...")
                method = getattr(self.extractor, method_name) 
                extracted_data[table_name] = method()
            except Exception as e:
                print(f"Failed to extract {table_name}: {e}")
        return extracted_data

    def load(self, table_data):
        """
        Lưu trữ dữ liệu vào PostgreSQL.
        :param table_data: Dictionary chứa các DataFrame cần lưu trữ.
        """
        print("Loading table data into PostgreSQL...")
        for table_name, df in table_data.items():
            try:
                print(f"Loading {table_name} into PostgreSQL...")
                self.loader.load_dataframe(df, table_name)
            except Exception as e:
                print(f"Failed to load {table_name}: {e}")

    def run_pipeline(self):
        """
        Chạy toàn bộ quy trình ETL (Extract -> Load).
        """
        print("Running ETL pipeline for table data...")
        extracted_data = self.extract()
        self.load(extracted_data)
        print("ETL pipeline for table data completed.")



class ETLText:
    def __init__(self, ticket_collection, mongo_uri, db_name, doc_dir):
        """
        Khởi tạo ETL pipeline cho dữ liệu dạng văn bản.
        :param ticket_collection: Danh sách các mã chứng khoán cần xử lý.
        :param mongo_uri: URI kết nối MongoDB.
        :param db_name: Tên database MongoDB.
        """
        self.ticket_collection = ticket_collection
        self.loader = MongoDBLoader(mongo_uri, db_name)
        self.embedding_model = TOOLS_CFG.embedding_model
        self.doc_dir = doc_dir
        self.db = self.loader.client[db_name]
    def extract(self):
        """
        Trích xuất dữ liệu từ các nguồn khác nhau (PDF, News, Social Media).
        :return: Một dictionary chứa các documents được trích xuất.
        """
        print("Extracting text data...")
        extracted_data = {
            "pdf_report": [],
            "news": [],
            "social_media": []
        }

        for ticket in self.ticket_collection:
            try:
                news_scraper = BaoChinhPhuScraper(id_company=ticket)
                news_scraper.search_articles()
                for article in news_scraper.data:
                    extracted_data["news"].append({
                        "ticker": ticket,
                        "source": "news",
                        "content": article["content"]
                    })

                social_media_scraper = ArticleScraper(symbol=ticket)
                social_media_data = social_media_scraper.scrape_articles()  
                for post in social_media_data:
                    extracted_data["social_media"].append({
                        "ticker": ticket,
                        "source": "social_media",
                        "content": post["content"]
                    })

                pdf_scraper = CafefPDFScraper(stock_symbol=ticket, headless=True, download_folder=self.doc_dir)
                pdf_scraper.search_disclosures()
                pdf_scraper.scrape_pdf_links()
                # pdf_scraper.download_all_pdfs()  
                pdf_links = pdf_scraper.pdf_links

                # pdf_files = [fn for fn in os.listdir(self.doc_dir) if fn.endswith('.pdf')]
                # for file_name in pdf_files:
                #     print(os.path.join(self.doc_dir, file_name))
                #     loader = PyPDFLoader(os.path.join(self.doc_dir, file_name))
                #     try:
                #         docs = loader.load_and_split()
                #     except Exception as e:
                #         print(f"Lỗi khi tải hoặc chia nhỏ tệp {file_name}: {e}")
                #         continue

                #     for doc in docs:
                #         extracted_data["pdf_report"].append({
                #             "ticker": ticket,
                #             "source": "pdf_report",
                #             "content": doc.page_content
                #         })

            except Exception as e:
                print(f"Failed to extract data for {ticket}: {e}")

        return extracted_data
    
    def transform(self, extracted_data):
        """
        Tạo vector embedding cho trường content của mỗi document.
        :param extracted_data: Dictionary chứa các documents đã trích xuất.
        :return: Dictionary chứa các documents đã được transform.
        """
        print("Transforming text data...")
        for source, documents in extracted_data.items():
            for doc in documents:
                try:
                    content = doc["content"]
                    embedding = self.embedding_model.embed_query(content)
                    doc["vector"] = embedding 
                except Exception as e:
                    print(f"Failed to transform document: {e}")
        return extracted_data

    def load(self, transformed_data):
        """
        Lưu trữ dữ liệu vào MongoDB.
        :param transformed_data: Dictionary chứa các documents đã được transform.
        """
        print("Loading text data into MongoDB...")
        for source, documents in transformed_data.items():
            try:
                collection = self.db[source]
                collection.insert_many(documents)
                print(f"✅ Loaded {len(documents)} documents into MongoDB collection: {source}")
            except Exception as e:
                print(f"Failed to load data into MongoDB collection {source}: {e}")



    def run_pipeline(self):
        print("Running ETL pipeline for text data...")
        extracted_data = self.extract()
        transformed_data = self.transform(extracted_data)
        self.load(transformed_data)
        print("ETL pipeline for text data completed.")




class FullETLPipeline:
    def __init__(self, ticket_collection, db_config, mongo_uri, db_name, html_contents, doc_dir):
        self.etl_table = ETLTable(ticket_collection, db_config)
        self.etl_text = ETLText(html_contents, mongo_uri, db_name, doc_dir)

    def run_pipeline(self):
        print("Running full ETL pipeline...")
        self.etl_table.run_pipeline()
        self.etl_text.run_pipeline()
        print("Full ETL pipeline completed.")