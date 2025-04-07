import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

PROJECT_ID = "gdsc2025"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

import vertexai
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Data/GDSC2025-ECOSCORE_AI/chatbot/gdsc2025-564ec12bcb03.json"

vertexai.init(project=PROJECT_ID, location=LOCATION)
from langchain_google_vertexai import VertexAIEmbeddings

# Initialize the a specific Embeddings Model version
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

# Create a vector store with a sample text
from langchain_core.vectorstores import InMemoryVectorStore

text = "LangChain is the framework for building context-aware reasoning applications"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings,
)

# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()

# Retrieve the most similar text
retrieved_documents = retriever.invoke("What is LangChain?")

# show the retrieved document's content
print(retrieved_documents[0].page_content)

text2 = (
    "LangGraph is a library for building stateful, multi-actor applications with LLMs"
)
two_vectors = embeddings.embed_documents([text, text2])
for vector in two_vectors:
    print(str(vector)[:100])  # Show the first 100 characters of the vector