import os
import yaml
from pyprojroot import here
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymongo
from backend.settings import PROJECT_CFG
os.environ['OPENAI_API_KEY'] = PROJECT_CFG.openai
from PIL import Image
import pytesseract

with open(here("config/tools_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

CHUNK_SIZE = app_config["document_rag_pdf"]["chunk_size"]
CHUNK_OVERLAP = app_config["document_rag_pdf"]["chunk_overlap"]
EMBEDDING_MODEL = app_config["document_rag_pdf"]["embedding_model"]
MONGODB_URI = os.getenv('MONGODB_URL') 
COLLECTION_NAME = app_config["document_rag_pdf"]["collection_name"]
DB_NAME = app_config["document_rag_pdf"]["db_name"]  
DOC_DIR = app_config["document_rag_pdf"]["unstructured_docs"]

class PrepareVectorDB:
    """
    Lớp này được sử dụng để chuẩn bị và quản lý một cơ sở dữ liệu vector (VectorDB) bằng cách sử dụng tài liệu từ một thư mục được chỉ định.
    Lớp này thực hiện các tác vụ sau:
    - Tải và chia nhỏ tài liệu (PDF).
    - Chia nhỏ văn bản thành các phần dựa trên kích thước và độ chồng chéo được chỉ định.
    - Nhúng các đoạn văn bản tài liệu bằng cách sử dụng một mô hình nhúng đã chỉ định.
    - Lưu trữ các vector đã nhúng vào một collection trong MongoDB.

    Thuộc tính:
        doc_dir (str): Đường dẫn đến thư mục chứa tài liệu (PDF) sẽ được xử lý.
        chunk_size (int): Kích thước tối đa của mỗi đoạn (tính bằng ký tự) mà văn bản tài liệu sẽ được chia nhỏ.
        chunk_overlap (int): Số ký tự chồng lấp giữa các đoạn liên tiếp.
        mongodb_uri (str): URI MongoDB để kết nối đến cơ sở dữ liệu.
        db_name (str): Tên của cơ sở dữ liệu MongoDB.
        collection_name (str): Tên của collection sẽ được sử dụng trong cơ sở dữ liệu MongoDB.

    Phương thức:
        path_maker(file_name: str, doc_dir: str) -> str:
            Tạo một đường dẫn đầy đủ bằng cách nối thư mục đã cho với tên tệp.

        run() -> None:
            Thực hiện quá trình đọc tài liệu, chia nhỏ văn bản, nhúng chúng thành vector và
            lưu cơ sở dữ liệu vector kết quả vào MongoDB.

        save_history_response_vectodb() -> None:
            Lưu trữ phản hồi của người dùng vào cơ sở dữ liệu vector (VectorDB) để truy vấn hoặc phân tích sau này.

    """

    def __init__(self,
                 doc_dir: str,
                 chunk_size: int,
                 chunk_overlap: int,
                 mongodb_uri: str,
                 db_name: str,
                 collection_name: str
                 ) -> None:

        self.doc_dir = doc_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = PROJECT_CFG.embedding_model
        self.mongodb_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name

        try:
            self.client = pymongo.MongoClient(self.mongodb_uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print("Connection to MongoDB successful")
        except pymongo.errors.ConnectionFailure as e:
            print(f"Connection failed: {e}")

   

    def path_maker(self, file_name: str, doc_dir):
        """
        Tạo một đường dẫn đầy đủ bằng cách nối thư mục và tên tệp.

        Tham số:
            file_name (str): Tên của tệp.
            doc_dir (str): Đường dẫn đến thư mục.

        Trả về:
            str: Đường dẫn đầy đủ của tệp.
        """
        return os.path.join(here(doc_dir), file_name)
    
    def save_history_response_vectodb(self, userid, response):
        """
        Lưu trữ phản hồi của người dùng vào cơ sở dữ liệu vector (VectorDB) để truy vấn hoặc phân tích sau này.
        
        Quy trình thực hiện:
        - Chia nhỏ phản hồi của người dùng thành các đoạn (sử dụng kích thước và độ chồng lấp).
        - Mỗi đoạn sẽ được nhúng thành một vector sử dụng mô hình nhúng đã chỉ định.
        - Lưu các vector nhúng vào MongoDB cùng với nội dung phản hồi và thông tin người dùng.
        
        Tham số:
            userid (str): ID của người dùng.
            response (str): Phản hồi từ người dùng cần lưu trữ.

        Trả về:
            None
        """

        try:
            vector = self.embedding_model.encode(response).tolist()
        except Exception as e:
            print(f"Lỗi khi nhúng đoạn văn bản trong tệp{e}")

        document = {
            "type": "history",
            "filetype":"historical_response",
            "response": response,  
            "content": response,
            "user_id": userid,
            "vector": vector,
        }
        try:
            self.collection.insert_one(document)
        except Exception as e:
            print(f"Lỗi khi lưu document vào MongoDB: {e}")

        print("Hoàn thành nhúng và phản hồi vào MongoDB.")

    def ocr(self,userid,type):
        file_list = [fn for fn in os.listdir(here(self.doc_dir)) if fn.endswith('.png') or fn.endswith('.jpg')]
        for file_name in file_list:
            image = Image.open(self.path_maker(file_name, self.doc_dir))
            extracted_text = pytesseract.image_to_string(image)
            try:
                vector = self.embedding_model.encode(extracted_text).tolist()
            except Exception as e:
                print(f"Lỗi khi nhúng đoạn văn bản trong tệp{e}")

            document = {
                "type": type,
                "filetype":"img",
                "file_name": file_name,
                "content": extracted_text,
                "user_id": userid,
                "vector": vector,
                }
            try:
                self.collection.insert_one(document)
            except Exception as e:
                print(f"Lỗi khi lưu document vào MongoDB: {e}")
            try:
                os.remove(self.path_maker(file_name, self.doc_dir))
                print(f"Đã xóa tệp {file_name} khỏi thư mục.")
            except Exception as e:
                print(f"Lỗi khi xóa tệp {file_name}: {e}")

            print("Hoàn thành nhúng và phản hồi vào MongoDB.")


    def run(self, type, userid=0):
        """
        Thực hiện logic chính để tạo và lưu các nhúng tài liệu vào MongoDB.

        Nếu collection chưa tồn tại:
        - Tải các tài liệu PDF từ `doc_dir`, chia nhỏ chúng thành các đoạn,
        - Nhúng các đoạn tài liệu bằng mô hình nhúng đã chỉ định,
        - Lưu các nhúng vào một collection trong MongoDB.

        Nếu collection đã có dữ liệu, quá trình tạo nhúng sẽ bị bỏ qua.

        In trạng thái tạo và số lượng vector trong collection MongoDB.

        Trả về:
            None
        """
        file_list = [fn for fn in os.listdir(here(self.doc_dir)) if fn.endswith('.pdf')]

        for file_name in file_list:
            loader = PyPDFLoader(self.path_maker(file_name, self.doc_dir))
            try:
                docs = loader.load_and_split()
            except Exception as e:
                print(f"Lỗi khi tải hoặc chia nhỏ tệp {file_name}: {e}")
                continue

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            )
            doc_splits = text_splitter.split_documents(docs)

            for doc_split in doc_splits:
                try:
                    vector = self.embedding_model.encode(doc_split.page_content).tolist()
                except Exception as e:
                    print(f"Lỗi khi nhúng đoạn văn bản trong tệp {file_name}: {e}")
                    continue
                
                document = {
                    "type" : type,
                    "filetype":"pdf",
                    "file_name": file_name,  
                    "content": doc_split.page_content,
                    "user_id": userid,
                    "vector": vector,
                }
                try:
                    self.collection.insert_one(document)
                except Exception as e:
                    print(f"Lỗi khi lưu document vào MongoDB: {e}")
                    continue

            print(f"Hoàn thành nhúng và lưu tệp {file_name} vào MongoDB.")
        # else:
        #     print(f"Tệp {file_name} đã tồn tại trong MongoDB. Bỏ qua xử lý.")
            try:
                os.remove(self.path_maker(file_name, self.doc_dir))
                print(f"Đã xóa tệp {file_name} khỏi thư mục.")
            except Exception as e:
                print(f"Lỗi khi xóa tệp {file_name}: {e}")
            # finally:
            #     self.client.close()
        print("Quá trình xử lý hoàn tất.")
        print("Số lượng vectors trong MongoDB collection:", self.collection.count_documents({}), "\n\n")

