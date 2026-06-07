from pypdf import PdfReader
from langchain_community.document_loaders import TextLoader

file_path = "AKS.txt"

def documentLoader(file_path:str)->str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
        documents = loader.load()
        return documents[0].page_content
    else:
        raise ValueError("Unsupported file format. Only PDF and TXT are supported.")