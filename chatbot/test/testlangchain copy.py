from langchain_google_vertexai import VertexAI
import os
from google.cloud import aiplatform

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Admin/Data/GDSC2025-ECOSCORE_AI/chatbot/gdsc2025-564ec12bcb03.json"
# To use model
aiplatform.init(project="gdsc2025", location="us-central1")
model = VertexAI(model_name="gemini-2.0-flash")


message = "Bạn có thể trả lời tốt tiếng việt không"
print(model.invoke(message))


# from langchain_google_vertexai import ChatVertexAI

# llm = ChatVertexAI(model="gemini-1.5-flash-001")
# await llm.ainvoke("hi")