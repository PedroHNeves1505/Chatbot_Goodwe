from pydantic import BaseModel, Field
from typing import Optional

class AnaliseConsulta(BaseModel):
    pergunta: str = Field(
        description='Entender a intenção principal do usuário'
        )
    aprovado: bool = Field(
        description='True se a resposta estiver correta, False caso contrário'
        )
    motivo: str = Field(
        description='Justificativa da aprovação ou detalhes do erro'
        )

class RespostaChat(BaseModel):
    pergunta_usuario: str = Field(
        description='Utilizar essa pergunta para entender contexto da resposta'
    )
    nome_empresa: str = Field(
        description="A empresa cuja resposta deve estar relacionada é a Goodwe"
    )
    pergunta_relevante: bool = Field(
        description="Indica se a pergunta tem relação com o carregador [ChargeGrid Intelligence] e [EV ChargeOps]"
    )
    topico_principal: Optional[str] = Field(
        description="Ter relação com o escopo definido do projeto"
    )
    rascunho_resposta: str = Field(
        description="A resposta inicial gerada pelo modelo para ser refinada pelo próximo passo."
    )