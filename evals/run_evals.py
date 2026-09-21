import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.guardrails.moderation import verificar_moderacao
from src.guardrails.scope_validator import validar_escopo
from src.chain.builder import executar_chatbot
from app import contar_tokens

def executar_avaliacoes():
    caminho_evals = os.path.join("evals", "eval_set.json")
    
    if not os.path.exists(caminho_evals):
        print(f"Erro: Arquivo {caminho_evals} não encontrado.")
        return

    with open(caminho_evals, "r", encoding="utf-8") as f:
        casos_teste = json.load(f)

    resultados = []
    print("Iniciando bateria de testes real (Evals)...\n")

    for teste in casos_teste:
        pergunta = teste["pergunta"]
        categoria = teste["categoria"]
        
        print(f"Testando [ID {teste['id']} - {categoria}]: {pergunta}")

        mod_check = verificar_moderacao(pergunta)
        if not mod_check["aprovado"]:
            status = "BLOQUEADO_MODERACAO"
            resposta = "Desculpe, não posso processar este tipo de solicitação por motivos de segurança."

        elif not validar_escopo(pergunta):
            status = "BLOQUEADO_ESCOPO"
            resposta = "Desculpe, como assistente do ecossistema GoodWe, só posso ajudar com questões sobre ChargeGrid Intelligence e EV ChargeOps."

        else:
            status = "APROVADO_E_PROCESSADO"
            try:
                resultado_chatbot = executar_chatbot(pergunta)
                resposta = getattr(resultado_chatbot, 'rascunho_resposta', str(resultado_chatbot))
            except Exception as e:
                resposta = f"Erro ao processar no LLM: {str(e)}"
                status = "ERRO_PROCESSAMENTO"

        resultado_caso = {
            "id": teste["id"],
            "categoria": categoria,
            "pergunta": pergunta,
            "status_sistema": status,
            "resposta_obtida": resposta,
            "tokens_resposta": contar_tokens(resposta) if resposta else 0
        }
        
        resultados.append(resultado_caso)
        print(f" -> Status: {status}\n")

    caminho_saida = os.path.join("evals", "sprint3_results.json")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"Testes reais finalizados! Resultados salvos com sucesso em: {caminho_saida}")

if __name__ == "__main__":
    executar_avaliacoes()