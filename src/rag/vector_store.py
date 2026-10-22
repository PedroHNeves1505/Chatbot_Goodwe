import hashlib
from langchain_core.documents import Document
from typing import Any
from langchain_chroma import Chroma
from src.rag.embeddings import get_embeddings

PERSIST_DIRECTORY = "db/chroma_db"

def vector_store():
    return Chroma(
        collection_name='chroma_db',
        embedding_function=get_embeddings(),
        persist_directory='db'
    )

def ids_generator(chunks: list[Document]) -> list[str]:
    ids = []
    for indice, chunk in enumerate(chunks):
        base = (
            f"{'chroma_bd'}|{chunk.metadata.get('source', '')}"
            f"|{chunk.metadata.get('page', '')}|{indice}|{chunk.page_content}"
        )
        ids.append(f"{'chroma_bd'}-{hashlib.sha256(base.encode('utf-8')).hexdigest()}")
    return ids

def salvar_chunks(chunks: list[Document]) -> Any:
    store = vector_store()
    ids = ids_generator(chunks)

    try:
        store.add_documents(chunks, ids=ids)
    except Exception:
        pass

    return store