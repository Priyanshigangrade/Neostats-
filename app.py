import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_chat_model
from models.embeddings import get_embedding_model
from utils.rag_utils import build_or_load_vectorstore, retrieve_context
from utils.web_search import search_web, should_search_web
from utils.prompting import build_system_prompt
from config.config import (
    GROQ_API_KEY,
    OPENAI_API_KEY,
    GOOGLE_API_KEY,
    TAVILY_API_KEY,
    KNOWLEDGE_BASE_PATH,
)


def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model"""
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]

        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))

        response = chat_model.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"


@st.cache_resource(show_spinner=False)
def get_cached_embedding_model():
    try:
        return get_embedding_model()
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_cached_vectorstore(_cache_buster: int):
    try:
        embedding_model = get_cached_embedding_model()
        if embedding_model is None:
            return None
        return build_or_load_vectorstore(embedding_model, rebuild=False)
    except Exception:
        return None


def get_available_providers():
    """Return providers with configured API keys"""
    try:
        providers = []
        if GROQ_API_KEY:
            providers.append("Groq")
        if OPENAI_API_KEY:
            providers.append("OpenAI")
        if GOOGLE_API_KEY:
            providers.append("Gemini")
        return providers
    except Exception:
        return []

def instructions_page():
    """Instructions and setup page"""
    st.title("The Chatbot Blueprint")
    st.markdown("Welcome! Follow these instructions to set up and run the complete chatbot solution.")
    
    st.markdown("""
    ## 🔧 Installation

    First, install the required dependencies: (Add Additional Libraries base don your needs)
    
    ```bash
    pip install -r requirements.txt
    ```
    
    ## API Key Setup
    
    You'll need API keys from your chosen provider. Get them from:
    
    ### OpenAI
    - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
    - Create a new API key
    - Set the variables in config
    
    ### Groq
    - Visit [Groq Console](https://console.groq.com/keys)
    - Create a new API key
    - Set the variables in config
    
    ### Google Gemini
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a new API key
    - Set the variables in config

    ### Tavily (for Live Web Search)
    - Visit [Tavily](https://app.tavily.com/)
    - Create API key
    - Set `TAVILY_API_KEY` in your environment

    ## 📚 Local Knowledge Base (RAG)

    - Create a folder named `knowledge_base` in your project root
    - Add local documents (`.txt`, `.md`, `.pdf`, `.csv`, `.json`)
    - Use **Rebuild RAG Index** in the chat sidebar after adding/updating docs
    
    ## 📝 Available Models
    
    ### OpenAI Models
    Check [OpenAI Models Documentation](https://platform.openai.com/docs/models) for the latest available models.
    Popular models include:
    - `gpt-4o` - Latest GPT-4 Omni model
    - `gpt-4o-mini` - Faster, cost-effective version
    - `gpt-3.5-turbo` - Fast and affordable
    
    ### Groq Models
    Check [Groq Models Documentation](https://console.groq.com/docs/models) for available models.
    Popular models include:
    - `llama-3.1-70b-versatile` - Large, powerful model
    - `llama-3.1-8b-instant` - Fast, smaller model
    - `mixtral-8x7b-32768` - Good balance of speed and capability
    
    ### Google Gemini Models
    Check [Gemini Models Documentation](https://ai.google.dev/gemini-api/docs/models/gemini) for available models.
    Popular models include:
    - `gemini-1.5-pro` - Most capable model
    - `gemini-1.5-flash` - Fast and efficient
    - `gemini-pro` - Standard model
    
    ## How to Use
    
    1. Go to the Chat page (sidebar navigation)
    2. Select provider and response mode
    3. Enable RAG and/or Live Web Search if needed
    4. Start chatting
    
    ## Tips
    
    - **Response Modes**: Toggle Concise vs Detailed output
    - **RAG**: Uses local knowledge base context first
    - **Live Search**: Triggers for latest/current info or when local context is missing
    - **Chat History**: Persists during your current session
    
    ## Troubleshooting
    
    - **API Key Issues**: Ensure key names and values are correctly exported
    - **Empty RAG Results**: Confirm your docs are in `knowledge_base/` and rebuild index
    - **Web Search Not Working**: Verify `TAVILY_API_KEY` and internet connectivity
    
    ---
    
    Ready to start chatting? Navigate to the **Chat** page from the sidebar.
    """)

def chat_page():
    """Main chat interface page"""
    try:
        st.title("🤖 NeoStats Smart Chatbot")

        available_providers = get_available_providers()
        if not available_providers:
            st.warning("No LLM provider API key found. Add `GROQ_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`.")
            return

        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "rag_cache_buster" not in st.session_state:
            st.session_state.rag_cache_buster = 0

        with st.sidebar:
            st.subheader("⚙️ Chat Settings")
            provider = st.selectbox("Provider", available_providers, index=0)
            response_mode = st.radio("Response Mode", ["Concise", "Detailed"], index=0)
            enable_rag = st.checkbox("Enable RAG (Local Docs)", value=True)
            enable_web_search = st.checkbox("Enable Live Web Search", value=True)

            if enable_rag:
                st.caption(f"Knowledge Base: {os.path.abspath(KNOWLEDGE_BASE_PATH)}")
                if st.button("🔄 Rebuild RAG Index", use_container_width=True):
                    try:
                        embedding_model = get_cached_embedding_model()
                        if embedding_model is None:
                            st.error("Embedding model failed to initialize.")
                        else:
                            build_or_load_vectorstore(embedding_model, rebuild=True)
                            st.session_state.rag_cache_buster += 1
                            st.success("RAG index rebuilt successfully.")
                    except Exception as e:
                        st.error(f"Failed to rebuild index: {str(e)}")

            if enable_web_search and not TAVILY_API_KEY:
                st.info("Set `TAVILY_API_KEY` to enable live web search.")

        provider_key = provider.lower()
        chat_model = get_chat_model(provider_key)

        vectorstore = None
        if enable_rag:
            vectorstore = get_cached_vectorstore(st.session_state.rag_cache_buster)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    rag_context = ""
                    rag_docs = []
                    web_context = ""

                    try:
                        if enable_rag and vectorstore is not None:
                            rag_context, rag_docs = retrieve_context(vectorstore, prompt)
                    except Exception:
                        rag_context, rag_docs = "", []

                    try:
                        if enable_web_search and should_search_web(prompt, has_rag_context=bool(rag_context)):
                            web_context = search_web(prompt)
                    except Exception:
                        web_context = ""

                    system_prompt = build_system_prompt(
                        response_mode=response_mode,
                        rag_context=rag_context,
                        web_context=web_context,
                    )
                    response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                    st.markdown(response)

                    with st.expander("Response Context", expanded=False):
                        st.write(f"RAG chunks used: {len(rag_docs)}")
                        st.write(f"Web search used: {'Yes' if bool(web_context) else 'No'}")

            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"Chat page failed: {str(e)}")

def main():
    try:
        st.set_page_config(
            page_title="NeoStats AI Chatbot Blueprint",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        with st.sidebar:
            st.title("Navigation")
            page = st.radio(
                "Go to:",
                ["Chat", "Instructions"],
                index=0
            )

            if page == "Chat":
                st.divider()
                if st.button("🗑️ Clear Chat History", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()

        if page == "Instructions":
            instructions_page()
        if page == "Chat":
            chat_page()
    except Exception as e:
        st.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()