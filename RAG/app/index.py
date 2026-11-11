from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
