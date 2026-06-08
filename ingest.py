from document_loader import document_loader
from splitter import split_documents
from embedding import create_vectorstore
import shutil
import os

file_path = "AKS.pdf"
chroma_dir = "chroma_db"

# delete old vectorstore if exists
if os.path.exists(chroma_dir):
    shutil.rmtree(chroma_dir)
    print("Old vectorstore deleted")

docs = document_loader(file_path)
print(f"Loaded {len(docs)} pages")          # ← check pages loaded
print(docs[0].page_content[:500])           # ← print first 500 chars of PDF

chunks = split_documents(docs)
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---")
    print(chunk.page_content)
print(f"Total chunks: {len(chunks)}")       # ← check chunks created

vectorstore = create_vectorstore(chunks, chroma_dir)
print("Document embedded successfully")
