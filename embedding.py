from config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from typing import List
from langchain_chroma import Chroma

#to create google_genai object for embedding
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="gemini-embedding-2", api_key=settings.GOOGLE_API_KEY)

# Create vectorstore from documents
def create_vectorstore(chunks:List[Document],persist_directory: str = "chroma_db")->Chroma:
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Vectorstore created with {len(chunks)} chunks")
    return vectorstore

# Load vectorstore from disk
def vectorload(persist_directory: str = "chroma_db")->Chroma:
    embeddings = get_embeddings()
    vectorstore = Chroma(
        collection_name="default",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    print("Vectorstore loaded from disk")
    return vectorstore