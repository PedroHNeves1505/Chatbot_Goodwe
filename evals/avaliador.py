import json
import os
import sys
from pathlib import Path

# Adiciona a raiz do projeto ao path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.chain.builder import executar_chatbot

def avaliar_resposta(resposta_ia: str, referencia: str, fontes: list) -> dict:
    """
    Fallback manual documentado (Rubrica 0 a 1) para Faithfulness e Answer Relevancy.
    """
    # 1. Faithfulness (Fidelidade ao contexto/referência e presença de citação)
    tem_citacao = len(fontes) > 0 or "Fonte:" in resposta_ia
    palavras_chave_ref = set(referencia.lower().split())
    palavras_chave_resp = set(resposta_ia.lower().split())
    
    intersecao = palavras_chave_ref.intersection(palavras_chave_resp)
    proporcao_cobertura = len(intersecao) / max(len(palavras_chave_ref), 1)
    
    faithfulness_score = 1.0 if (proporcao_cobertura > 0.4 and tem_citacao) else (0.7 if proporcao_cobertura > 0.2 else 0.3)
    
    # 2. Answer Relevancy (Relevância da resposta em relação à pergunta esperada)
    relevancy_score = 1.0 if proporcao_cobertura > 0.3 else 0.5

    return {
        "faithfulness": round(faithfulness_score, 2),
        "answer_relevancy": round(relevancy_score, 2),
        "tem_citacao": tem_citacao
    }

def executar_avaliador():
    caminho_dataset = Path(__file__).resolve().parent / "eval_dataset.json"
    
    if not caminho_dataset.exists():
        print("Dataset de avaliação não encontrado.")
        return

    with open(caminho_dataset, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print(f"Iniciando avaliação em lote de {len(dataset)} perguntas...\n")
    
    resultados_totais = []
    soma_faith = 0
    soma_rel = 0

    for item in dataset:
        pergunta = item["pergunta"]
        referencia = item["referencia_esperada"]
        
        print(f"Testando ID {item['id']}: {pergunta}")
        
        # Executa o pipeline RAG real do projeto
        try:
            resposta_obj = executar_chatbot(pergunta)
            resposta_texto = getattr(resposta_obj, "resposta_final", str(resposta_obj))
            fontes = getattr(resposta_obj, "fontes", [])
        except Exception as e:
            print(f"Erro ao executar chatbot: {e}")
            resposta_texto = "Erro"
            fontes = []

        # Calcula as métricas do fallback manual
        scores = avaliar_resposta(resposta_texto, referencia, fontes)
        
        soma_faith += scores["faithfulness"]
        soma_rel += scores["answer_relevancy"]
        
        print(f"   -> Faithfulness: {scores['faithfulness']} | Relevancy: {scores['answer_relevancy']} | Citação Visível: {scores['tem_citacao']}\n")
        
        resultados_totais.append({
            "id": item["id"],
            "pergunta": pergunta,
            "resposta": resposta_texto,
            "scores": scores
        })

    media_faith = soma_faith / len(dataset)
    media_rel = soma_rel / len(dataset)
    
    print("="*40)
    print(f"RESULTADO FINAL DA AVALIAÇÃO (Iteração RAG):")
    print(f"Média Faithfulness: {media_faith:.2f}")
    print(f"Média Answer Relevancy: {media_rel:.2f}")
    print("="*40)
    
    # Salva o relatório de scores na pasta evals/
    relatorio_path = Path(__file__).resolve().parent / "relatorio_scores.json"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        json.dump({
            "media_faithfulness": round(media_faith, 2),
            "media_answer_relevancy": round(media_rel, 2),
            "detalhes": resultados_totais
        }, f, ensure_ascii=False, indent=4)
    print(f"Relatório salvo em: {relatorio_path}")

if __name__ == "__main__":
    executar_avaliador()