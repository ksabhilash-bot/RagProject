from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List

# Function to create a retriever from the Chroma vectorstore
def get_retriever(vectorstore:Chroma,k:int =4):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        }
    )


# Function to retrieve relevant documents based on a query for manual testing
def retrieve_docs(retriever, query: str) -> List[Document]:
    docs = retriever.invoke(query)
    print(f"Retrieved {len(docs)} chunks for query: '{query}'")
    return docs