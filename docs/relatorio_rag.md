# RELATÓRIO DE EVOLUÇÃO DO PROJETO — SPRINT 04

Projeto: Chatbot com IA para Mobilidade Elétrica — GoodWe (EV Challenge)<br>

Disciplina: Prompt and Artificial Intelligence · 2º Semestre CC — 2026.2<br>
Parceiro: GoodWe Brasil<br>

Professor: Jorge Luiz Gomes<br>

---

## 1. Resumo da Evolução
O projeto evoluiu de uma arquitetura estática e monolítica até um sistema RAG de nível corporativo e mensurável:

* Sprints 1 e 2: Concepção da arquitetura inicial, prompts monolíticos embutidos no código e lógica de parsing frágil em expressões regulares.

* Sprint 3: Refatoração conversacional utilizando LCEL (LangChain Expression Language), Pydantic para saídas estruturadas, isolamento de prompts em arquivos Markdown (prompts/) e estruturação inicial da pasta de testes (evals/).

* Sprint 4 (Atual): Elevação do chatbot a um estado medido, confiável e utilizável através da integração de um pipeline RAG end-to-end com ChromaDB persistente, embeddings nomic-embed-text via Ollama, grounding estrito com citação visível de fontes, guardrails de segurança e escopo, interface web em Flask e métricas de avaliação quantitativa.

---

## 2. Pipeline RAG e Decisões de Arquitetura

A infraestrutura foi modularizada na pasta src/rag/ e src/chain/, destacando-se as seguintes escolhas técnicas:

* Carregamento e Chunking: Emprego de PyMuPDFLoader para leitura dos manuais técnicos oficiais (como o 2023-11-03907711.pdf / GoodWe HCA) e RecursiveCharacterTextSplitter para fatiamento otimizado de textos.

* Carregamento e Chunking: Emprego de PyMuPDFLoader para leitura dos manuais técnicos oficiais (como o 2023-11-03907711.pdf / GoodWe HCA) e RecursiveCharacterTextSplitter para fatiamento otimizado de textos.

* Desacoplamento e Tipagem Estrita: Manutenção dos prompts em arquivos Markdown e validação robusta por schemas Pydantic (AnaliseConsulta e RespostaChat), assegurando que o modelo retorne JSONs perfeitamente formatados para o backend e interface web.

---

## 3. Tabela de Comparativo Antes / Depois

|Critério de Avaliação|Sprints 1 / 2|Sprint 3|Sprint 04|
| :--- | :---: | :---: | ---: |
|Base de Conhecimento |Estática / Hardcoded no código |Estática + Histórico de Conversação |Base expandida em ChromaDB persistente com manuais oficiais
|Recuperação de Contexto |Inexistente |Limitada ao histórico de chat |Recuperação semântica dinâmica via embeddings nomic-embed-text
|Presença de Citação |Nenhuma citação de fonte |Nenhuma citação de fonte |Citação visível de documento e página em toda resposta
|Segurança e Escopo |Sem validação prévia |Filtros básicos de conversação |Guardrails ativos
|Métrica de Avaliação |Testes manuais ad-hoc |Testes estruturados sem métricas de RAG |Faithfulness: 1.00 / Answer Relevancy: 1.00
|Interface de Acesso |Flask |Flask |Flask

---

# 4. Problemas Encontrados e Soluções Adotadas

1- Problema de Importação Relativa (ImportError: attempted relative import with no known parent package)

* Contexto: Ao executar scripts individuais de ingestão diretamente de subpastas (python src/rag/loader.py), o interpretador perdia o escopo do pacote raiz.

* Solução: Padronização da execução via módulo com a flag -m a partir da raiz do projeto (python -m src.rag.loader), garantindo a resolução correta de dependências relativas.

2- Truncamento de Respostas Técnicas e Citações Incompletas

* Contexto: As primeiras gerações do Ollama eram interrompidas no meio de listas técnicas devido ao limite restritivo de tokens (num_predict).

* Solução: Elevação do parâmetro num_predict para 1024 tokens na configuração do modelo e refinamento do prompt versionado, garantindo a completude das especificações do carregador HCA G2 e a exibição correta das fontes.

3- Conflito de Variáveis Literais em JSON no LangChain Template (Herança Sprint 3)

* Contexto: A conversão de prompts contendo exemplos em JSON gerava erros de compilação de variáveis no LangChain.   

* Solução: Substituição das chaves de exemplo por descrições textuais diretas e isolamento estrito das variáveis reais de template ({history}, {pergunta}, {format_instructions}).  

--- 

## 5. Equipe e Divisão de Trabalho

|Nome Completo |RM |Tarefa Principal no Projeto
| :-- | :--: | --: |
|Akin Alexandre Mendes Martins |572553 |Refatoração para LCEL, integração do ChromaDB e vetorização com Ollama. 
|Maria Eduarda Rocha Benjamim |570544 |Engenharia de Prompts, criação dos arquivos .md e testes de jailbreak e escopo.
|Pedro Henrique Neves |571382 |Elaboração do dataset de avaliação (eval_set.json), métricas de eval e interface web