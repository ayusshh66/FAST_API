from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

#pdf loader
# 
loader = PyPDFLoader(str(pdf_path)) 
