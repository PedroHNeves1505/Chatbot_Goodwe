from pydantic import BaseModel, Field

class AnaliseConsulta(BaseModel):
    pergunta: str = Field(
        description='Reescreva a pergunta exata feita pelo usuário de forma clara e limpa. NUNCA coloque frases de status como "aguardando entrada" ou saudações.'
    )
    aprovado: bool = Field(
        description='True se a pergunta tiver relação com os escopos da GoodWe, False caso contrário'
    )
    motivo: str = Field(
        description='Justificativa breve da aprovação ou recusa'
    )