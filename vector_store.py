import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
DATA_PATH = "data/debales_docs.txt"
INDEX_PATH = "faiss_index"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def create_vector_store():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            "data/debales_docs.txt not found. Please run scraper.py first."
        )

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    if not text.strip():
        raise ValueError("Scraped data file is empty.")

    docs = [Document(page_content=text)]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(INDEX_PATH)

    print("Vector store created successfully.")
    print(f"Total chunks stored: {len(chunks)}")

def load_vector_store():
    embeddings = get_embeddings()

    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

if __name__ == "__main__":
    create_vector_store()