from embedding import vectorload
from retriever import get_retriever
from chain import build_chain, ask

chroma_dir = "chroma_db"

vectorstore = vectorload(chroma_dir)
retriever = get_retriever(vectorstore)
chain = build_chain(retriever)

print("RAG Assistant Ready. Type 'exit' to quit.\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    response = ask(chain, question)
    print(f"AI: {response}\n")