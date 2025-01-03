from fastapi import FastAPI
from pydantic import BaseModel
from agent import chatbot, agent

app = FastAPI()


# Define the request body model
class MessageRequest(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/chat")
async def chat(request: MessageRequest):
    res = await chatbot({"messages": [request.message]})
    return res


@app.post("/search")
async def search(request: MessageRequest):
    res = await agent.ainvoke({"messages": [request.message]})
    return res["response"]
