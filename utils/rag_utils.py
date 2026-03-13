import os
from typing import List, Tuple

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config.config import (
    KNOWLEDGE_BASE_PATH,
    VECTOR_DB_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
)


SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".pdf"}


def load_local_documents(folder_path: str = KNOWLEDGE_BASE_PATH) -> List[Document]:
    """Load local documents from knowledge base folder"""
    try:
        if not os.path.exists(folder_path):
            return []

        documents: List[Document] = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                try:
                    file_path = os.path.join(root, file_name)
                    extension = os.path.splitext(file_name)[1].lower()
                    if extension not in SUPPORTED_EXTENSIONS:
                        continue

                    if extension == ".pdf":
                        loader = PyPDFLoader(file_path)
                    else:
                        loader = TextLoader(file_path, encoding="utf-8")

                    documents.extend(loader.load())
                except Exception:
                    continue

        return documents
    except Exception as e:
        raise RuntimeError(f"Failed to load local documents: {str(e)}")


def chunk_documents(documents: List[Document]) -> List[Document]:
    """Split long documents into chunks for vector indexing"""
    try:
        if not documents:
            return []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        return splitter.split_documents(documents)
    except Exception as e:
        raise RuntimeError(f"Failed to chunk documents: {str(e)}")


def build_or_load_vectorstore(embedding_model, rebuild: bool = False):
    """Build or load Chroma vector store"""
    try:
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)

        if rebuild:
            docs = load_local_documents()
            chunks = chunk_documents(docs)
            if not chunks:
                return None

            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory=VECTOR_DB_PATH,
            )
            return vectorstore

        vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embedding_model,
        )
        return vectorstore
    except Exception as e:
        raise RuntimeError(f"Failed to build/load vectorstore: {str(e)}")


def retrieve_context(vectorstore, query: str, top_k: int = TOP_K) -> Tuple[str, List[Document]]:
    """Retrieve relevant context from vector DB"""
    try:
        if vectorstore is None:
            return "", []

        retrieved_docs = vectorstore.similarity_search(query, k=top_k)
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        return context_text, retrieved_docs
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve context: {str(e)}")