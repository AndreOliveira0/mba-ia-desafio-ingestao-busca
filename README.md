# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto consiste em um sistema de RAG (Retrieval-Augmented Generation) que permite a ingestão de documentos PDF em um banco de dados vetorial e a realização de consultas semânticas via linha de comando (CLI).

O sistema utiliza modelos de linguagem para responder perguntas baseadas exclusivamente no conteúdo do documento fornecido.

---

# 📋 Requisitos e Regras de Negócio

Para garantir a fidelidade das respostas, o software segue estas diretrizes:

* **Ingestão de Dados:** O PDF é processado em pedaços (chunks) de 1000 caracteres com overlap de 150 caracteres.
* **Busca Vetorial:** O sistema recupera os 10 resultados mais relevantes (`k=10`) utilizando a métrica de similaridade do pgVector.
* **Fidelidade ao Contexto:** A IA responde apenas com base no contexto fornecido pelo PDF.
* **Tratamento de Perguntas Fora de Contexto:** Caso a resposta não esteja no documento, o sistema responderá obrigatoriamente:

```text
Não tenho informações necessárias para responder sua pergunta.
```

* **Restrições de Comportamento:** É proibido inventar informações, usar conhecimento externo ou emitir opiniões.

---

# 🚀 Tecnologias Obrigatórias

## Stack Principal

* **Linguagem:** Python
* **Framework:** LangChain
* **Banco de Dados:** PostgreSQL com extensão pgVector
* **Infraestrutura:** Docker e Docker Compose

## Modelos OpenAI

* **LLM:** `gpt-5-nano`
* **Embeddings:** `text-embedding-3-small`

## Modelos Gemini

* **LLM:** `gemini-3.1-flash-lite-preview`
* **Embeddings:** `models/embedding-001`

---

# 📁 Estrutura do Projeto

```text
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   ├── chat.py
├── document.pdf
└── README.md
```

---

# 🛠️ Como Executar

## 1. Clonar o Projeto

```bash
git clone https://github.com/AndreOliveira0/mba-ia-desafio-ingestao-busca
cd mba-ia-desafio-ingestao-busca
```

---

## 2. Configurar o Ambiente Python

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python3 -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

## 4. Variáveis de Ambiente

Crie o arquivo `.env`:

```bash
cp .env.example .env
```

### Exemplo OpenAI

```env
OPENAI_API_KEY=your_api_key_here
```

### Exemplo Gemini

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## 5. Iniciar o Banco de Dados

```bash
docker compose up -d
```

---

## 6. Realizar a Ingestão do PDF

```bash
python src/ingest.py
```

---

## 7. Executar o Chat

```bash
python src/chat.py
```

---

# 💬 Exemplos de Interação

## Pergunta no Contexto

### Entrada

```text
Qual o faturamento da empresa?
```

### Resposta

```text
O faturamento foi de X milhões.
```

---

## Pergunta Fora de Contexto

### Entrada

```text
Qual a capital da França?
```

### Resposta

```text
Não tenho informações necessárias para responder sua pergunta.
```

---

# ✅ Objetivo do Projeto

Este projeto demonstra:

* Ingestão de documentos PDF
* Vetorização de conteúdo textual
* Busca semântica utilizando pgVector
* Construção de pipelines RAG com LangChain
* Uso de modelos de linguagem com restrição de contexto
* Execução local com Docker e PostgreSQL

---

# 📌 Observações

* O sistema responde exclusivamente com base no conteúdo indexado.
* Perguntas sem correspondência semântica suficiente retornam a resposta padrão obrigatória.
* O armazenamento vetorial utiliza PostgreSQL com extensão pgVector.

---

# 📄 Licença

Projeto destinado para fins acadêmicos e educacionais.
