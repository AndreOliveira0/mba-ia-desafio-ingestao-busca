import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_embeddings():
    openaikey = os.getenv("OPENAI_API_KEY")
    googlekey = os.getenv("GOOGLE_API_KEY")

    if openaikey:
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif googlekey:
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    else:
        raise ValueError("Por favor, defina OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env.")

def get_model():
    openaikey = os.getenv("OPENAI_API_KEY")
    googlekey = os.getenv("GOOGLE_API_KEY")

    if openaikey:
        return ChatOpenAI(model=os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano"), temperature=0)
    elif googlekey:
        return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM_MODEL", "gemini-3.1-flash-lite-preview"), temperature=0)
    else:
        raise ValueError("Por favor, defina OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env.")

def retrieve_context(input_data):
  question = input_data["question"]
  embeddings = get_embeddings()

  store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
  )

  results = store.similarity_search_with_score(question, k=10)

  context = "\n\n".join([f"Texto: {doc.page_content} (Score: {score:.4f})\n" for doc, score in results])
  
  return {"contexto": context, "pergunta": question}

def search_prompt():
  runnable_retrieve_context = RunnableLambda(retrieve_context)

  prompt = PromptTemplate(
    input_variables=["contexto", "pergunta"],
    template=PROMPT_TEMPLATE
  )

  model = get_model()
  
  chain = runnable_retrieve_context | prompt | model | StrOutputParser()
  
  return chain