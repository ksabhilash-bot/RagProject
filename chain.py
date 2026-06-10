import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma

load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_chain(retriever):
    llm = ChatMistralAI(
        api_key=os.getenv("MISTRAL_API_KEY"),
        model="mistral-large-latest",
        temperature=0.3
    )

    prompt = ChatPromptTemplate.from_template("""
        You are a smart assistant representing Abhilash K S — a Full-Stack Developer and MCA student.
        You help visitors on his portfolio website learn about him in a natural, conversational way.

        Use the context below to answer the question. 
        - Respond directly and naturally — no meta-commentary like "based on the context" or "according to the information provided".
        - Write as if you genuinely know Abhilash and are speaking on his behalf.
        - Keep answers concise and friendly, 2-4 sentences unless detail is needed.
        - If the context does not contain enough information, respond naturally:
          "That's not something I have details on right now — feel free to reach out to Abhilash directly at ksabhilash11111@gmail.com"
        - Never say "based on the context", "according to the context", "the context says", or similar phrases.

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
    text = question.strip().lower()

    small_talk = {
        "ok": "You're welcome! Feel free to ask anything about Abhilash, his projects, skills, or services.",
        "okk": "You're welcome! Feel free to ask anything about Abhilash, his projects, skills, or services.",
        "okkk": "You're welcome! Feel free to ask anything about Abhilash, his projects, skills, or services.",
        "okay": "Glad I could help! Let me know if you have any questions.",
        "thanks": "You're welcome! 😊",
        "thank you": "You're welcome! 😊",
        "thx": "You're welcome! 😊",
        "hmm": "Is there anything else you'd like to know about Abhilash?",
        "great": "Glad to hear that! Feel free to ask more questions.",
        "nice": "Thank you! Let me know if you'd like to know more.",
        "cool": "😎 Happy to help!",
        "bye": "Goodbye! Feel free to come back anytime.",
        "hello": "Hello! Ask me anything about Abhilash, his projects, skills, or services.",
        "hi": "Hi! How can I help you today?"
    }

    if text in small_talk:
        return small_talk[text]
    response = chain.invoke(question)
    return response