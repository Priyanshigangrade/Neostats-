import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import EMBEDDING_MODEL_NAME


def get_embedding_model():
	"""Initialize and return embedding model used for RAG"""
	try:
		embedding_model = HuggingFaceEmbeddings(
			model_name=EMBEDDING_MODEL_NAME,
			model_kwargs={"device": "cpu"},
			encode_kwargs={"normalize_embeddings": True},
		)
		return embedding_model
	except Exception as e:
		raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")
