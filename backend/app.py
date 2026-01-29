from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from contextlib import asynccontextmanager
from seed import seed_database
import threading


# 1. Lifespan: What to do on Startup/Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Nexus AI Backend Starting...")
    
    # Run seeding in a separate thread so it doesn't block the API from starting
    # (This ensures the container passes health checks while the DB is still waking up)
    thread = threading.Thread(target=seed_database)
    thread.start()
    
    yield
    # Shutdown logic (optional cleanup)
    print("🛑 Nexus AI Backend Stopping...")

# 2. Initialize App with Lifespan
app = FastAPI(lifespan=lifespan)

# CORS set-up
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],                      # POST, OPTIONS, etc.
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def health_check():
    return {"status": "active", "service": "Grapg-LLM core"}

@app.post("/chat")
async def chat(request: QueryRequest):
    response = run_agent(request.query)
    return response