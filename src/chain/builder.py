from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.schemas.AnaliseConsulta import AnaliseConsulta
from src.schemas.RespostaChat import RespostaChat
from src.rag.retriever import retrive_generator
from .memoria import memoria_buffer
import os
from dotenv import load_dotenv

load_dotenv()

def carregar_prompt(nome_arquivo: str) -> str:
    caminho = os.path.join("prompts", nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

llm = ChatOllama(
    model=os.environ['OLLAMA_MODEL'],
    base_url=os.environ['OLLAMA_HOST'],
    temperature=0,
    num_predict=1024
)

PROMPT_ANALISE = carregar_prompt("system_prompt_analise_v2.md")
PROMPT_RESPOSTA = carregar_prompt("system_prompt_resposta_v2.md")

prompt_analise = ChatPromptTemplate.from_template(PROMPT_ANALISE + "\n\n{format_instructions}")
parser_analise = PydanticOutputParser(pydantic_object=AnaliseConsulta)
chain_analise = prompt_analise | llm | parser_analise

prompt_resposta = ChatPromptTemplate.from_template(PROMPT_RESPOSTA + "\n\n{format_instructions}")
parser_resposta = PydanticOutputParser(pydantic_object=RespostaChat)
chain_resposta = prompt_resposta | llm | parser_resposta

def formatar_docs(docs) -> str:
    formatados = []
    for doc in docs:
        fonte = doc.metadata.get("source", "Desconhecido")
        pagina = doc.metadata.get("page", "?")
        formatados.append(f"[Fonte: {fonte} | Página: {pagina}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatados)

def executar_chatbot(pergunta_usuario: str):
    historico_atual = memoria_buffer.load_memory_variables({})['history']
    
    analise = chain_analise.invoke({
        'pergunta': pergunta_usuario,
        'history': historico_atual,
        'format_instructions': parser_analise.get_format_instructions()
    })
    pergunta_processada = analise.pergunta
    
    retriever = retrive_generator(k=4)
    docs_recuperados = retriever.invoke(pergunta_processada)
    contexto_recuperado = formatar_docs(docs_recuperados)
    
    resposta = chain_resposta.invoke({
        'pergunta_usuario': pergunta_processada,
        'history': historico_atual,
        'context': contexto_recuperado, 
        'format_instructions': parser_resposta.get_format_instructions()
    })
    
    return resposta