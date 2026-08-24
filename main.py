from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import ChatRequest, ChatResponse

from services.embedding_service import create_embedding
from services.pinecone_service import search_pinecone
from services.llm_service import generate_answer


# Create FastAPI application
app = FastAPI(
    title="WebDevInsight RAG API"
)


# Allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "WebDevInsight RAG API is running"
    }


# Chat endpoint
@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # Step 1: Create embedding for user question
    question_embedding = create_embedding(
        request.question
    )

    # Step 2: Search Pinecone
    retrieved_context = search_pinecone(
        question_embedding
    )

    # Step 3: Send question + context to Groq
    answer = generate_answer(
        request.question,
        retrieved_context
    )

    # Step 4: Return answer
    return ChatResponse(
        answer=answer
    )