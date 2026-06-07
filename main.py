from config import settings
from langchain_mistralai import ChatMistralAI
from document_loader import documentLoader
from langchain_core.prompts import ChatPromptTemplate

file_path = "AKS.txt"
document_text = documentLoader(file_path)


template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI assistant for AKS Pvt. Limited.

        Answer the user's question using ONLY the provided context.

        If the answer is not present in the context, say:
        "I could not find that information in the company documents."

        Be concise and accurate.
        
        Context:
        {context}
        """
    ),
    ("human", "{input}")
])

prompt = template.format_prompt(context=document_text, input="What is AKS?")

model = ChatMistralAI(model="mistral-small-2603", api_key=settings.MISTRAL_API_KEY)
result = model.invoke(prompt)
print(result.content)