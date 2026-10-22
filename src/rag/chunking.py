from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_em_chunks(documentos: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size =1000,
        chunk_overlap =200,
        separators=['\n\n', '\n', '. ', ' ', '']
    )

    chunks = splitter.split_documents(documentos)
    return chunks