def validar_escopo(texto: str) -> bool:
    if not texto:
        return False

    texto_lower = texto.lower()

    palavras_chave_permitidas = [
        "goodwe", "chargegrid", "chargeops", "hca", "g2", "carregador", 
        "recarga", "potência", "kw", "kwh", "tarifa", "pico", "solar", 
        "inversor", "frotas", "veículo", "eletroposto", "bateria", "energia",
        "powergrid", "temperatura", "segurança", "sobrecarga"
    ]

    saudacoes = ["olá", "ola", "bom dia", "boa tarde", "boa noite", "oi", "tudo bem"]
    if any(saudacao in texto_lower for saudacao in saudacoes):
        return True

    for palavra in palavras_chave_permitidas:
        if palavra in texto_lower:
            return True

    return False