from config import settings
from document_loader import document_loader
from splitter import split_documents
from embedding import create_vectorstore,vectorload
from retriever import get_retriever, retrieve_docs
import os
from chain import build_chain, ask

file_path = "AKS.pdf"
chroma_dir = "chroma_db"

if os.path.exists(chroma_dir):
    vectorstore = vectorload(chroma_dir)
else:
    docs = document_loader(file_path)
    chunks = split_documents(docs)
    vectorstore = create_vectorstore(chunks, chroma_dir)

retriever = get_retriever(vectorstore)
chain = build_chain(retriever)

# ask questions
response = ask(chain, "what are the departments?")
print("ai: ",response)





# template = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
#         You are an AI assistant for AKS Pvt. Limited.

#         Answer the user's question using ONLY the provided context.

#         If the answer is not present in the context, say:
#         "I could not find that information in the company documents."

#         Be concise and accurate.
        
#         Context:
#         {context}
#         """
#     ),
#     ("human", "{input}")
# ])

# prompt = template.format_prompt(context=docs, input="What is AKS?")

# model = ChatMistralAI(model="mistral-small-2603", api_key=settings.MISTRAL_API_KEY)
# result = model.invoke(prompt)
# print(result.content)