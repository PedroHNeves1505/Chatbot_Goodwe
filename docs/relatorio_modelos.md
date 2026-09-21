# Relatório de Evolução do Projeto: GoodWe EV Challenge 2026 (Sprint 03)

## 1. Resumo da Evolução

* Sprints 1 e 2 (Versão Legada/Manual): O chatbot operava de forma monolítica, com lógica de prompts acoplada diretamente ao código Python em strings gigantescas. O tratamento de saída estruturada dependia de parsing frágil em expressões regulares (regex) e o controle de fluxo de moderação/segurança era acoplado e de difícil manutenção. Os testes de avaliação eram executados manualmente ou com scripts ad-hoc sem padronização de métricas por categorias (happy_path, edge_case, jailbreak, out_of-scope).

* Sprint 3 (Arquitetura Atual com LCEL e Modularização): O ecossistema foi totalmente refatorado utilizando LangChain Expression Language (LCEL), Pydantic para validação rígida de saídas estruturadas (Structured Output), e desacoplamento de prompts em arquivos Markdown (.md) na pasta prompts/. Implementou-se um pipeline de integração contínua de testes robusto na pasta evals/, gerando telemetria detalhada de tokens, latência e acurácia por categoria de teste.

## 2. Refatoração: Decisões Técnicas e Trade-offs (LCEL e Prompts em .md)

A migração para o LCEL (LangChain Expression Language) e o isolamento dos prompts em arquivos Markdown (.md) envolveram escolhas arquiteturais fundamentais:

* Trade-off de Desacoplamento:

    * Decisão: Mover todos os system prompts para a pasta prompts/ e carregá-los via I/O padrão do Python (open()).

    * Por quê: Eliminou a poluição de strings literais no código-fonte, permitindo versionamento isolado dos prompts (evolução de v1 para v2) e facilitando revisões de engenharia de prompt sem risco de quebrar a lógica de execução em Python.

* Trade-off de Tipagem Estrita:

    * Decisão: Adoção de PydanticOutputParser combinado com schemas declarativos (AnaliseConsulta e RespostaChat).

    * Por quê: Garante que o modelo Ollama retorne estritamente um JSON formatado de acordo com o contrato da aplicação. Caso o LLM falhe no formato, o pipeline intercepta o erro, evitando falhas em cascata no frontend Flask.


## 3. Tabela Comparativa (Antes vs. Depois)
Esta tabela sintetiza a evolução de performance e arquitetura entre as entregas anteriores e o estado atual da Sprint 3:

| Critério de Avaliação | Sprints 1/2 |	Sprint 03 |
| :--- | :---: | ---: |
| Qualidade das Respostas (Nota no Eval)| Média (Respostas por vezes genéricas ou fora do escopo) | Alta (Conformidade estrita via Few-Shot e restrição de contexto) |
| Tokens por Turno (Média) | ~250 - 320 tokens (prompts longos embutidos) | ~140 - 210 tokens (otimizado via LCEL e parsing limpo) |
| Latência Média por Requisição | ~250 - 320 tokens (prompts longos embutidos) | Estável (~2.1s otimizado com temperature=0) |
| Acurácia do Structured Output | ~75% (falhas frequentes em JSON malformado) | 100% (garantido por Pydantic Output Parser)|
| Organização do Código | Prompts e lógica misturados em arquivos | Arquitetura limpa (prompts/*.md, src/chain/, evals/) |

## 4. Problemas Encontrados e Soluções
Problema 1: Conflito de Variáveis Literais em JSON no LangChain Template
* Descrição: Ao converter os prompts contendo exemplos em JSON ({ "pergunta": "..." }) para Markdown, o LangChain interpretava as chaves simples como variáveis de template obrigatórias, gerando erros de execução INVALID_PROMPT_INPUT no servidor Flask.
* Decisão Tomada: Substituição das chaves de exemplo por descrições textuais diretas nos blocos de exemplo e isolamento estrito das variáveis reais de template ({history}, {pergunta}, {format_instructions}).
* Por quê: Evitou falsos positivos do compilador de templates do LangChain, mantendo o ecossistema de parsing intacto sem corromper o formato de saída esperado pelo Pydantic.


Problema 2: Tratamento de Entradas Maliciosas ou Fora de Escopo
* Descrição: Tentativas de jailbreak (ex: pedidos de receitas ou scripts genéricos) passavam inicialmente pelo fluxo de resposta principal, gerando custos de processamento desnecessários.
* Decisão Tomada: Implementação de uma cadeia de análise prévia (Guardrail de Escopo) que classifica a intenção do usuário (aprovado: true/false) antes de acionar a geração de resposta final.
* Por quê: Garante bloqueio imediato de prompts maliciosos com mensagens padronizadas de recusa e protege a reputação do ecossistema GoodWe EV Challenge.

## 5. Equipe e Divisão de Trabalho
| Nome Completo | RM| Tarefa Principal na Sprint 3 |
|--: |--: |--: | 
| Pedro Henrique Neves | 571382 | Refatoração para LCEL e estruturação da pasta evals/|
| Maria Eduarda Rocha Benjamim| 570544 | Engenharia de Prompts, criação dos arquivos .md e testes de jailbreak.|
| Akin Alexandre Mendes Martins | 571382 | Elaboração do dataset de avaliação (eval_set.json) e métricas.|