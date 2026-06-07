import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(retriever):
    llm = ChatMistralAI(
        api_key=os.getenv("MISTRAL_API_KEY"),
        model="mistral-large-latest",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant. Answer the question based only on the context provided.
        If the answer is not in the context, say "I don't have enough information to answer this."

        Context:
        {context}

        Question:
        {question}

        Answer:
    """)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def ask(chain, question: str) -> str:
    response = chain.invoke(question)
    return response