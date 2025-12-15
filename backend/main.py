
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.rag import Retriever, Generator
from backend.stackoverflow_client import StackOverflowClient
from backend.database import initialize_database, get_db_session
from backend.models import QuestionAnswer
from backend.ai_assist import AIResponse

app = FastAPI(title="StackOverflowAI Backend API")

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Initialize DB and models
DATABASE_URL = os.getenv("STACKOVERFLOW_DATA_PATH", "sqlite:///./data/stackoverflow.db")
db_session = get_db_session(DATABASE_URL)
initialize_database(db_session)

# Initialize StackOverflow Client (stub for API or data dump interaction)
so_client = StackOverflowClient(api_key=os.getenv("STACKOVERFLOW_API_KEY"))

# Initialize Retriever and Generator for RAG + LLM
retriever = Retriever(db_session=db_session)
generator = Generator(api_key=os.getenv("OPENAI_API_KEY"))


class Query(BaseModel):
    query: str
    top_k: int = 5


class ChatMessage(BaseModel):
    user: str
    message: str


@app.get("/")
async def root():
    return {"message": "Welcome to StackOverflowAI backend API"}


@app.post("/api/ask", response_model=AIResponse)
async def ask_stackoverflowai(query: Query):
    """
    Endpoint to ask a question in natural language and get AI-generated answer.
    Uses RAG: retrieves relevant Q&A, then generates an answer with attribution.
    """
    # Retrieve relevant Q&A
    relevant_qa = retriever.retrieve(query.query, top_k=query.top_k)
    if not relevant_qa:
        raise HTTPException(status_code=404, detail="No relevant data found.")

    # Generate answer using retrieved data as context
    try:
        answer, sources = generator.generate_answer(query.query, relevant_qa)
        return AIResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/api/questions/{question_id}", response_model=QuestionAnswer)
async def get_question(question_id: int):
    """
    Get detailed Q&A entry by ID.
    """
    qa = db_session.query(QuestionAnswer).filter(QuestionAnswer.id == question_id).first()
    if not qa:
        raise HTTPException(status_code=404, detail="Question not found")
    return qa


@app.post("/api/chat", response_model=List[AIResponse])
async def chat(messages: List[ChatMessage]):
    """
    Simple chat endpoint to handle interactive sessions.
    This is a stub for chatroom or conversational interface.
    """
    # For demo, just reply with generated answer to last message
    if not messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    last_message = messages[-1].message
    relevant_qa = retriever.retrieve(last_message, top_k=3)
    answer, sources = generator.generate_answer(last_message, relevant_qa)
    return [AIResponse(answer=answer, sources=sources)]
```

```plaintext
