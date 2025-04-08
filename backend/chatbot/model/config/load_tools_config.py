import os
import yaml
from pyprojroot import here
from backend.settings import PROJECT_CFG



class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("config/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Set environment variables
        os.environ['OPENAI_API_KEY'] = PROJECT_CFG.openai
        os.environ['TAVILY_API_KEY'] = PROJECT_CFG.tavily
        self.stock_db = PROJECT_CFG.postgrest_dbms


        # Primary agent
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Internet Search config
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])

        # Document RAG configs
        self.user_rag_llm_temperature = float(
            app_config["document_rag_pdf"]["llm_temperature"])
        self.user_rag_embedding_model = app_config["document_rag_pdf"]["embedding_model"]
        self.user_rag_k = app_config["document_rag_pdf"]["k"]
        self.user_db_name = app_config["document_rag_pdf"]["db_name"]
        self.user_rag_collection_name = app_config["document_rag_pdf"]["collection_name"]
        self.user_rag_mongodb_url=PROJECT_CFG.mongodb_uri
        self.user_doc_rag_chunk_overlap=app_config["document_rag_pdf"]["chunk_overlap"]
        self.user_doc_rag_chunk_size=app_config["document_rag_pdf"]["chunk_size"]
        self.user_doc_rag_unstructured_docs=app_config["document_rag_pdf"]["unstructured_docs"]

        # Document RAG Admin configs
        self.admin_rag_llm_temperature = float(
            app_config["document_rag_pdfAdmin"]["llm_temperature"])
        self.admin_rag_embedding_model = app_config["document_rag_pdfAdmin"]["embedding_model"]
        self.admin_db_name = app_config["document_rag_pdfAdmin"]["db_name"]
        self.admin_rag_k = app_config["document_rag_pdfAdmin"]["k"]
        self.admin_rag_collection_name = app_config["document_rag_pdfAdmin"]["collection_name"]
        self.admin_rag_mongodb_url=PROJECT_CFG.mongodb_uri
        
        # History RAG configs
        self.history_rag_llm_temperature = float(
            app_config["chatbot_history"]["llm_temperature"])
        # self.history_rag_embedding_model = app_config["chatbot_history"]["embedding_model"]
        # self.history_rag_vectordb_directory = str(here(
        #     app_config["chatbot_history"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.history_rag_k = app_config["chatbot_history"]["k"]
        self.history_rag_collection_name = app_config["chatbot_history"]["collection_name"]
        self.history_rag_db_name = app_config["chatbot_history"]["db_name"]


        #SQL Agent configs
        self.sqldb_directory = str(here(
            app_config["sqlagent_configs"]["sqldb_dir"]))
        self.sqlagent_llm = app_config["sqlagent_configs"]["llm"]
        self.sqlagent_llm_temperature = float(
            app_config["sqlagent_configs"]["llm_temperature"])

        #SQL Agent configs
        self.funcagent_llm = app_config["funcagent_configs"]["llm"]
        self.funcagent_llm_temperature = float(
            app_config["funcagent_configs"]["llm_temperature"])

        # Graph configs
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])
        
TOOLS_CFG = LoadToolsConfig()
