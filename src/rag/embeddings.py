from langchain_community.embeddings import OllamaEmbeddings
import os

model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

def get_embeddings():
    OllamaEmbeddings(
        model=model
    )