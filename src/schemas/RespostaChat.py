from pydantic import BaseModel, Field
from typing import Optional

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
    resposta_final: str = Field(
        description="Faça a repsosta final da forma mais resumida e direta ao ponto possível"
    )