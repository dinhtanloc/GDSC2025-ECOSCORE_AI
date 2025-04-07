from pydantic import BaseModel
import configs.settings
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
from pymongo import MongoClient
from backend.backend.settings import MEDIA_ROOT
from chatbot.models.utils.prepare_vectodb import PrepareVectorDB
from chatbot.models.utils.memory import Memory
from backend.backend.config import LoadProjectConfig
from jose import JWTError, jwt
# from chatbot.models.utils.memory import ChatHistory
from fastapi import Request, Response
from chatbot.models.chatbot_backend import ChatBot

PROJECT_CFG=LoadProjectConfig()
SECRET_KEY = PROJECT_CFG.djangoprj
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

class ChatRequest(BaseModel):
    message: str

class CurrentUser(BaseModel):
    user_id: int
    username: str
    email: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        email = payload.get("email")

        if user_id is None or username is None or email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return CurrentUser(user_id=user_id, username=username, email=email)


@app.post("/chatbot/interact/")
async def interact(current_user: CurrentUser = Depends(get_current_user),  chat_request: ChatRequest = None):
    """
    Handle chatbot interaction via POST request.
    """
    chatbots = {}

    if not chat_request:
        raise HTTPException(status_code=400, detail="Invalid request data")
    user_message = chat_request.message
    user_id = current_user.user_id
    

    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    if user_id not in chatbots:
        thread_id = str(uuid.uuid4())
        chatbots[user_id] = ChatBot(user_id=user_id, thread_id=thread_id)
    chatbot = chatbots[user_id]
    chatbot_history = []
    try:
        print(chatbot_history, user_message, user_id, chatbot.thread_id)
        _, updated_chat = chatbot.respond(chatbot_history, user_message)
        bot_response = updated_chat[-1][1] if updated_chat else 'No response'
    except Exception as e:
        print(e)
        return Response({'error': f'Error processing request: {str(e)}'}, status=500)
    return {"response": bot_response, "thread_id": thread_id}


@app.get("/chatbot/history")
async def get_chat_history(current_user: CurrentUser = Depends(get_current_user)):
    """
    Retrieve chat history for the authenticated user.
    """
    try:
        # chat_history = ChatHistory.objects.filter(user=current_user.user_id).order_by('-timestamp').values()
        return {"chat_history": list({})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")


@app.post("/upload/file")
async def upload_file(file: UploadFile = File(...), current_user: CurrentUser = Depends(get_current_user)):
    file_type = file.content_type
    directory = "pdf" if file_type == "application/pdf" else "images"
    save_path = os.path.join(PROJECT_CFG["userdata_docdir"], directory)

    os.makedirs(save_path, exist_ok=True)
    file_location = os.path.join(save_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file_type == "application/pdf":
        prepare_vectordb = PrepareVectorDB(
            doc_dir=f"{PROJECT_CFG.userdata_docdir}/{directory}",
            chunk_size=PROJECT_CFG.userdata_chunksize,
            chunk_overlap=PROJECT_CFG.userdata_chunk_overlap,
            mongodb_uri=PROJECT_CFG.userdata_mongodb_uri,
            db_name=PROJECT_CFG.userdata_dbname,
            collection_name=PROJECT_CFG.userdata_collection,
        )
        prepare_vectordb.run(userid=current_user.user_id, type="user")
    elif file_type.startswith("image/"):
        prepare_vectordb = PrepareVectorDB(
            doc_dir=f"{PROJECT_CFG.userdata_docdir}/{directory}",
            chunk_size=PROJECT_CFG.userdata_chunksize,
            chunk_overlap=PROJECT_CFG.userdata_chunk_overlap,
            mongodb_uri=PROJECT_CFG.userdata_mongodb_uri,
            db_name=PROJECT_CFG.userdata_dbname,
            collection_name=PROJECT_CFG.userdata_collection,
        )
        prepare_vectordb.ocr(userid=current_user.user_id, type="user")

    return JSONResponse(
        status_code=200,
        content={"message": "File uploaded successfully", "file_url": file_location},
    )


@app.post("/upload/admin-data")
async def upload_admin_data(file: UploadFile = File(...), current_user: CurrentUser = Depends(get_current_user)):
    file_type = file.content_type
    directory = "admin"
    save_path = os.path.join(PROJECT_CFG["admindata_docdir"], directory)

    os.makedirs(save_path, exist_ok=True)
    file_location = os.path.join(save_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file_type == "application/pdf":
        prepare_vectordb = PrepareVectorDB(
            doc_dir=PROJECT_CFG.admindata_docdir,
            chunk_size=PROJECT_CFG.admindata_chunksize,
            chunk_overlap=PROJECT_CFG.admindata_chunk_overlap,
            mongodb_uri=PROJECT_CFG.admindata_mongodb_uri,
            db_name=PROJECT_CFG.admindata_dbname,
            collection_name=PROJECT_CFG.admindata_collection,
        )
        prepare_vectordb.run(type=directory)
        return JSONResponse({"message": "PDF file uploaded successfully", "file_url": file_location}, status_code=200)

    elif file_type in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        engine = create_engine(PROJECT_CFG.postgrest_dbms)
        try:
            if file_type == "text/csv":
                data = pd.read_csv(file_location)
            else:
                data = pd.read_excel(file_location)

            rows, cols = data.shape
            table_name = os.path.splitext(os.path.basename(file_location))[0]
            data.to_sql(table_name, engine, if_exists="replace", index=False)

            return JSONResponse(
                {
                    "message": "CSV or XLSX file uploaded successfully",
                    "file_url": file_location,
                    "rows": rows,
                    "columns": cols,
                },
                status_code=200,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")


@app.get("/protected")
async def read_protected_data(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, user {current_user}. This is protected data."}

@app.get("/use")
async def read_protected_data():
    return {"message": f"Hello, user This is protected data."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)