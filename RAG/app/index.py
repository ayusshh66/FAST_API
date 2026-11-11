from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

#pdf loader
loader = PyPDFLoader(str(pdf_path)) 
docs = loader.load()

#split the docs into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)

#embedding the chunks using openAi embedding
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#create a vector store 
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection_local",
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"]
)

print("vector store created and documents embedded successfully")