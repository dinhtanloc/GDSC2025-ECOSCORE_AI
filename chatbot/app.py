from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict
from fastapi import HTTPException
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

class Question(BaseModel):
    question: str

@app.post("/answer")
def answer_question(question_data: Question):
    answer = f"Your question was: '{question_data.question}'. This is the answer!"
    return {"answer": answer}

class OpenAIClient:
    def __init__(self, api_key):
        self.client = 'openai'

    def chat(self, messages):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return completion.choices[0].message.content


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]



@app.post("/chat/")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        response = 'openai_client.chat(chat_request.messages)'
        return JSONResponse({
            "content": response,
            "role": "assistant"
            })
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)