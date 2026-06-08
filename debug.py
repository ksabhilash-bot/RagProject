from embedding import vectorload
from retriever import get_retriever, retrieve_docs

vectorstore = vectorload("chroma_db")
retriever = get_retriever(vectorstore)

docs = retrieve_docs(retriever, "who is the CEO of AKS Pvt. Limited")
for doc in docs:
    print("---")
    print(doc.page_content)