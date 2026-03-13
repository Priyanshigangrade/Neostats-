import os
import sys
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    GOOGLE_API_KEY,
    GEMINI_MODEL,
)


def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing. Set it in your environment.")
        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0.2,
        )
        return groq_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")


def get_chatopenai_model():
    """Initialize and return the OpenAI chat model"""
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing. Set it in your environment.")
        openai_model = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=OPENAI_MODEL,
            temperature=0.2,
        )
        return openai_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize OpenAI model: {str(e)}")


def get_chatgemini_model():
    """Initialize and return the Gemini chat model"""
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Set it in your environment.")
        gemini_model = ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model=GEMINI_MODEL,
            temperature=0.2,
        )
        return gemini_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {str(e)}")


def get_chat_model(provider: str):
    """Factory to return chat model by provider name"""
    try:
        normalized_provider = provider.strip().lower()
        if normalized_provider == "groq":
            return get_chatgroq_model()
        if normalized_provider == "openai":
            return get_chatopenai_model()
        if normalized_provider in ["gemini", "google"]:
            return get_chatgemini_model()
        raise ValueError(f"Unsupported provider: {provider}")
    except Exception as e:
        raise RuntimeError(f"Failed to get chat model: {str(e)}")