from fastapi import APIRouter

router = APIRouter(prefix="/ask", tags=["ask query to thru RAG"])

@router.post("/")
async def query(question:str):
    return {
        "question": question,
        "answer": "answer"
    }