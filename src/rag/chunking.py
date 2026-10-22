import re
import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

_CABECALHO = re.compile(
    r"fonte\s*:\s*(?P<fonte>[^|]+?)\s*\|\s*page\s*:\s*(?P<pagina>\d+)"
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CORPUS_PATH = Path(os.getenv("CORPUS_PATH", BASE_DIR / "data" / "knowledge_base"))

def carregar_docs() -> list[Document]:
    arquivos = list(CORPUS_PATH.glob("*.pdf"))

    documentos: list[Document] = []
    fonte_atual, pagina_atual = None, 0
    paragrafo: list[str] = []

    for arquivo in arquivos:
        loader = PyPDFLoader(str(arquivo))
        docs_do_pdf = loader.load()

        for doc in docs_do_pdf:
            fonte_atual = doc.metadata.get("source", arquivo)
            pagina_atual = doc.metadata.get("page", 0) + 1
            texto_pag = doc.page_content

            documentos.append(doc)


    def fechar_paragrafo() -> None:
        nonlocal fonte_atual, pagina_atual
        texto = " ".join(paragrafo).strip()
        if texto:
            documentos.append(
                Document(
                    page_content=texto,
                    metadata={"source": fonte_atual, "page": pagina_atual},
                )
            )
        paragrafo.clear()

    for linha in texto_pag.splitlines():
        limpa = linha.strip()
        if not limpa or limpa.startswith("#"):
            fechar_paragrafo()
            continue
        if limpa.startswith("---"):
            fechar_paragrafo()
            cabecalho = _CABECALHO.search(limpa)
            if cabecalho:
                fonte_atual = cabecalho.group("fonte").strip()
                pagina_atual = int(cabecalho.group("pagina"))
            continue
        paragrafo.append(limpa)

    fechar_paragrafo()
    print(f"[ingest] {len(documentos)} documentos carregados de {arquivo.name}")
    return documentos

def dividir_em_chunks(documentos: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size =1000,
        chunk_overlap =200,
        separators=['\n\n', '\n', '. ', ' ', '']
    )

    chunks = splitter.split_documents(documentos)
    return chunks