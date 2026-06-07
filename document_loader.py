from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

def document_loader(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        return loader.load()

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
        return loader.load()

    else:
        raise ValueError(
            "Unsupported file format. Only PDF and TXT are supported."
        )