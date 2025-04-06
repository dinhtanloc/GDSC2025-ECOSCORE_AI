from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict
from fastapi import HTTPException
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List
import os
import uuid
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import pytesseract
from pydantic import BaseModel
from pymongo import MongoClient
from backend.backend.config import LoadProjectConfig
PROJECT_CFG=LoadProjectConfig()

# import openai
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ChatHistory(BaseModel):
    user_id: str
    message: str
    thread_id: str


@app.post("/chatbot/interact")
async def interact(chat_history: ChatHistory, token: str = Depends(oauth2_scheme)):
    """
    Handle chatbot interaction via POST request.
    """
    user_message = chat_history.message
    user_id = chat_history.user_id
    thread_id = chat_history.thread_id or str(uuid.uuid4())

    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    # Simulate chatbot logic (replace with your actual ChatBot implementation)
    bot_response = f"Bot response to: {user_message}"
    return {"response": bot_response, "thread_id": thread_id}


@app.get("/chatbot/history")
async def get_chat_history(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Retrieve chat history for the authenticated user.
    """
    chat_history = [{"message": "Hello", "timestamp": "2023-10-01T12:00:00Z"}]
    return chat_history


@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    """
    Upload a file (PDF or image) and process it.
    """
    file_type = file.content_type
    directory = "pdf" if file_type == "application/pdf" else "images"
    save_path = os.path.join(PROJECT_CFG["userdata_docdir"], directory)

    os.makedirs(save_path, exist_ok=True)
    file_location = os.path.join(save_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file_type == "application/pdf":
        # Process PDF (replace with your PrepareVectorDB logic)
        pass
    elif file_type.startswith("image/"):
        # Process image using OCR
        text = pytesseract.image_to_string(Image.open(file_location))
        print(f"Extracted text: {text}")

    return JSONResponse(
        status_code=200,
        content={"message": "File uploaded successfully", "file_url": file_location},
    )


@app.post("/upload/admin-data")
async def upload_admin_data(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    """
    Upload admin data (PDF, CSV, or XLSX) and process it.
    """
    file_type = file.content_type
    directory = "admin"
    save_path = os.path.join(PROJECT_CFG["admindata_docdir"], directory)

    os.makedirs(save_path, exist_ok=True)
    file_location = os.path.join(save_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file_type == "application/pdf":
        # Process PDF (replace with your PrepareVectorDB logic)
        pass
    elif file_type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        engine = create_engine(PROJECT_CFG["postgrest_dbms"])
        try:
            if file_type == "text/csv":
                data = pd.read_csv(file_location)
            else:
                data = pd.read_excel(file_location)

            rows, cols = data.shape
            table_name = os.path.splitext(os.path.basename(file_location))[0]
            data.to_sql(table_name, engine, if_exists="replace", index=False)

            return JSONResponse(
                status_code=200,
                content={
                    "message": "CSV or XLSX file uploaded successfully",
                    "file_url": file_location,
                    "rows": rows,
                    "columns": cols,
                },
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    raise HTTPException(status_code=400, detail="Unsupported file type")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)