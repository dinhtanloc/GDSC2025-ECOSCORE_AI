import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

PROJECT_ID = "gdsc2025"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

import vertexai
# Đặt đường dẫn đến tệp chứng thực của Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Data/GDSC2025-ECOSCORE_AI/backend/gdsc2025-d0c2645d360f.json"

# Khởi tạo Vertex AI với ID dự án và vị trí
vertexai.init(project=PROJECT_ID, location=LOCATION)
from langchain_google_vertexai import VertexAIEmbeddings

# Khởi tạo một phiên bản mô hình Embedding cụ thể
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

# Tạo kho vector với một đoạn văn bản mẫu
from langchain_core.vectorstores import InMemoryVectorStore

text = "LangChain là khung làm việc để xây dựng các ứng dụng suy luận có ngữ cảnh"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings,
)

# Sử dụng kho vector như một bộ truy xuất
retriever = vectorstore.as_retriever()

# Truy xuất đoạn văn bản tương tự nhất
retrieved_documents = retriever.invoke("LangChain là gì?")

# Hiển thị nội dung tài liệu đã truy xuất
print(retrieved_documents[0].page_content)

text2 = (
    "LangGraph là thư viện để xây dựng các ứng dụng đa tác nhân có trạng thái với LLM"
)
# Tạo hai vector biểu diễn cho hai đoạn văn bản
two_vectors = embeddings.embed_documents([text, text2])
for vector in two_vectors:
    print(str(vector)[:100])  # Hiển thị 100 ký tự đầu tiên của vector
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import VertexAI

message = "Bạn có thể trả lời tốt tiếng việt không"
model = VertexAI(model_name="gemini-2.0-flash")

print(model.invoke(message))
llm = ChatVertexAI(model="gemini-2.0-flash")
print(llm.invoke(message))