def verificar_moderacao(texto: str) -> dict:
    if not texto or not isinstance(texto, str):
        return {"aprovado": False, "motivo": "Texto vazio ou inválido."}

    texto_lower = texto.lower()

    padroes_jailbreak = [
        "esqueça todas as instruções",
        "ignore previous instructions",
        "você agora é um",
        "act as",
        "modo desenvolvedor",
        "developer mode",
        "system prompt"
    ]

    for padrao in padroes_jailbreak:
        if padrao in texto_lower:
            return {
                "aprovado": False, 
                "motivo": "Tentativa de manipulação de prompt (jailbreak) detectada."
            }

    palavras_proibidas = ["palavrao1", "palavrao2"]
    for palavra in palavras_proibidas:
        if palavra in texto_lower:
            return {
                "aprovado": False, 
                "motivo": "Termo impróprio ou ofensivo detectado."
            }

    return {"aprovado": True, "motivo": "Mensagem aprovada na moderação."}