
import os

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import ChatOllama


load_dotenv()

router = APIRouter(
    prefix="/query",
    tags=["query"]
)


# Request body
class QueryRequest(BaseModel):
    question: str


# Use the SAME embedding model as index.py
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to the EXISTING Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection_local",
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"]
)


# Local LLM - no OpenAI API key needed
llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


@router.post("/")
def query(request: QueryRequest):

    question = request.question

    # Step 1: Search for relevant PDF chunks
    search_results = vector_db.similarity_search(
        query=question,
        k=4
    )

    formatted_output=[]

    for result in search_results:
        page = result.metadata.get("page",0)+1
        text = result.page_content

        output = f"[Page: {page}] {text}"
        formatted_output.append(output)

    # Step 2: Build context from retrieved chunks
    context = "\n\n".join(formatted_output)

    # Step 3: Create prompt
    system_prompt = f"""
You are a helpful assistant that answers questions
using only the provided PDF context.

If the context does not contain the answer,
respond with "I don't know."

Include the page number when applicable.

Context:
{context}
"""

    # Step 4: Ask the local LLM
    response = llm.invoke([
        ("system", system_prompt),
        ("human", question)
    ])

    return {
        "question": question,
        "answer": response.content
    }
