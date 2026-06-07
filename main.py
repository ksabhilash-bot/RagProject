from config import settings

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2603", api_key=settings.MISTRAL_API_KEY)
result = model.invoke("hello whats your name?")
print(result.content)