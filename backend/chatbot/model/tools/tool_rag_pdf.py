# from langchain_Mongodb import Mongodb
from backend.settings import PROJECT_CFG
from langchain_core.tools import tool
from chatbot.model.config.load_tools_config import TOOLS_CFG
from chatbot.model.utils.prepare_vectodb import PrepareVectorDB
import os


class UserDocumentRAGTool:
    """
    Một công cụ để truy xuất các tài liệu liên quan được tải lên bởi người dùng, sử dụng phương pháp Tạo Dữ Liệu Tăng Cường Truy Xuất (RAG) với các vector embeddings.

    Công cụ này sử dụng một mô hình embedding của OpenAI đã được huấn luyện trước để chuyển đổi các truy vấn thành các biểu diễn dạng vector. Các vector này sau đó được sử dụng để truy vấn cơ sở dữ liệu vector MongoDB nhằm truy xuất top-k tài liệu hoặc mục nhập có liên quan nhất từ một bộ sưu tập cụ thể. Dữ liệu trong đây chỉ được chia sẻ đối với từng user id cụ thể, không được công khai rộng rãi
    Dữ liệu trong cơ sở dữ liệu MongoDB sẽ được trả về theo cấu trúc sau:
        document = {
                "type"(str) : Phân loại  trong cơ sở dữ liệu, nếu type=user thì dữ liệu trong cơ sở dữ liệu sẽ được bảo mật với nhau, nếu type="admin" thì dữ liệu có thể được phân bổ rộng rãi 
                "filetype" (str): Định dạng loại dữ liệu, "img" hoặc "pdf",
                "file_name" (str): Tên file được lưu dô cơ sở dữ liệu
                "content" (str): Nội dung văn bản được lưu
                "user_id" (int): mã số user, nếu type="admin" thì user_id=0
                "vector" (array): vector database
        }

    Các thuộc tính:
    embedding_model (str): Tên của mô hình embedding OpenAI được sử dụng để tạo ra các biểu diễn vector của các truy vấn.
    vectordb_dir (str): Thư mục nơi cơ sở dữ liệu vector Mongodb được lưu trữ trên đĩa. Thư mục này luôn được chỉ đến nơi lưu trữ tài liệu của người dùng
    k (int): Số lượng tài liệu lân cận gần nhất (tài liệu có liên quan nhất) sẽ được truy xuất từ cơ sở dữ liệu vector.
    vectordb (Mongodb): Thể hiện cơ sở dữ liệu vector Mongodb được kết nối với bộ sưu tập và mô hình embedding đã chỉ định.
    Các phương thức:
    __init__: Khởi tạo công cụ bằng cách thiết lập mô hình embedding, cơ sở dữ liệu vector, và các tham số truy xuất.
    """

    def __init__(self, mongodb_uri:str, db_name:str, k: int, collection_name: str) -> None:
        """
        Khởi tạo công cụ UserDocumentRAGTool với cấu hình cần thiết.

        Tham số:
        mongodb_uri (str): Đường dẫn kết nối đến database của MongoDB, nơi lưu trữ dữ liệu và kiến thức
        db_name (str): Dataset, nơi chứa dữ liệu cụ thể cho từng chức năng khác nhau
        k (int): Số lượng tài liệu lân cận gần nhất sẽ được truy xuất dựa trên sự tương đồng của truy vấn.
        collection_name (str): Tên của bộ sưu tập trong cơ sở dữ liệu vector chứa các tài liệu do người dùng tải lên.
        """
        self.name = "lookup_user_document"
        self.embedding_model = PROJECT_CFG.embedding_model
        self.db_name=db_name
        self.mongodb_uri=mongodb_uri
        self.k = k
        self.vectordb = PrepareVectorDB(
            doc_dir=TOOLS_CFG.user_doc_rag_unstructured_docs,
            chunk_size=TOOLS_CFG.user_doc_rag_chunk_size,
            chunk_overlap=TOOLS_CFG.user_doc_rag_chunk_overlap,
            mongodb_uri=self.mongodb_uri,
            db_name=self.db_name,
            collection_name=collection_name
        )
        # print("Number of vectors in vectordb: ", self.vectordb.collection.count(), "\n\n")

    def similarity_search(self, query: str, k: int = None):
        """
        Thực hiện tìm kiếm tài liệu tương tự bằng cách sử dụng truy vấn từ người dùng.

        Tham số:
        query (str): Truy vấn để tìm kiếm tài liệu.
        k (int, tùy chọn): Số lượng tài liệu lân cận gần nhất sẽ được trả về. Nếu không cung cấp, sẽ sử dụng giá trị mặc định của đối tượng.

        Trả về:
        list: Danh sách các tài liệu phù hợp.
        """
        # embedding_model = OpenAIEmbeddings(model=self.embedding_model)
        query_vector = self.embedding_model.encode(query).tolist()

        if query_vector is None:
            return "Invalid query or embedding generation failed."

        if k is None:
            k = self.k

        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_vector,
                "path": "vector",
                "numCandidates": 400,
                "limit": k,
                }
            }

        unset_stage = {
            "$unset": "vector"
        }

        project_stage = {
            "$project": {
                "content": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }

        pipeline = [vector_search_stage, unset_stage, project_stage]

        # Execute the search
        try:
            results = self.vectordb.collection.aggregate(pipeline)
            self.vectordb.client.close()
        except Exception as e:
            print(e)
        return list(results)
       


@tool('lookup_user_document')
def lookup_user_document(query: str) -> str:
    """Tìm kiếm các tài liệu đã tải lên của người dùng để tìm thông tin liên quan dựa trên truy vấn."""
    rag_tool = UserDocumentRAGTool(
        mongodb_uri= TOOLS_CFG.user_rag_mongodb_url,
        db_name=TOOLS_CFG.user_db_name,
        k=TOOLS_CFG.user_rag_k,
        collection_name=TOOLS_CFG.user_rag_collection_name
    )
    results = rag_tool.similarity_search(query, k=rag_tool.k)
    search_result = ""
    for result in results:
        print('---result', result)
        search_result += f"Content: {result.get('content', 'N/A')}\n"
    return search_result