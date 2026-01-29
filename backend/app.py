from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: QueryRequest):
    response = run_agent(request.query)
    return response