import os
from dotenv import load_dotenv
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def get_embeddings():
    openaikey = os.getenv("OPENAI_API_KEY")
    googlekey = os.getenv("GOOGLE_API_KEY")

    if openaikey:
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    elif googlekey:
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    else:
        raise ValueError("Por favor, defina OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env.")

def ingest_pdf():
    current_dir = Path(__file__).parent
    pdf_path = current_dir.parent / os.getenv("PDF_PATH")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    split_docs = splitter.split_documents(docs)

    embeddings = get_embeddings()

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
        pre_delete_collection=True
    )

    print(f"Ingesting {len(split_docs)} chunks into PGVector...")
    store.add_documents(split_docs)
    print("Ingestion complete.")


if __name__ == "__main__":
    ingest_pdf()