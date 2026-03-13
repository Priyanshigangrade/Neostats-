# NeoStats AI Chatbot - Quick Start Guide

## ✅ API Keys Configuration

Your Groq and Tavily API keys need to be set as environment variables:
- **GROQ_API_KEY**: Get from https://console.groq.com/keys
- **TAVILY_API_KEY**: Get from https://app.tavily.com/

## 🚀 How to Run

### Option 1: Using Python Script (Recommended - Cross-platform)
```bash
python3 run.py
```

### Option 2: Using Shell Script (macOS/Linux)
```bash
./run.sh
```

### Option 3: Manual Environment Setup
```bash
export GROQ_API_KEY='your_groq_api_key_here'
export TAVILY_API_KEY='your_tavily_api_key_here'
streamlit run app.py
```

## 📋 Project Features

### ✅ Implemented Features
1. **Multi-Provider LLM Support**
   - Groq ✅ (Currently configured)
   - OpenAI
   - Google Gemini

2. **RAG (Retrieval-Augmented Generation)**
   - Local document loading (`.txt`, `.md`, `.pdf`, `.csv`, `.json`)
   - Chroma vector database for embeddings
   - Intelligent context retrieval
   - One-click "Rebuild RAG Index" button

3. **Live Web Search**
   - Tavily API integration ✅ (Currently configured)
   - Smart triggering for freshness queries
   - Fallback when local context insufficient

4. **Response Modes**
   - **Concise**: Short, summarized replies (3-6 lines)
   - **Detailed**: Thorough, in-depth responses with explanations

5. **UI Features**
   - Clean Streamlit interface
   - Provider/mode selection sidebar
   - Chat history persistence
   - Response context transparency
   - RAG index rebuild button
   - Clear chat history button

## 📚 Using RAG (Local Documents)

1. Create sample documents in the `knowledge_base/` folder:
   ```bash
   mkdir -p knowledge_base
   echo "Your document content here" > knowledge_base/sample.txt
   ```

2. In the app sidebar, click **"Rebuild RAG Index"**

3. Now your local documents will be referenced in responses

## 🔧 Customization

### Change LLM Models
Edit `config/config.py`:
```python
GROQ_MODEL = "llama-3.1-70b-versatile"  # Change to other Groq models
```

### Adjust RAG Chunking
```python
CHUNK_SIZE = 1000        # Size of text chunks
CHUNK_OVERLAP = 150      # Overlap between chunks
TOP_K = 4                # Number of chunks to retrieve
```

## 📁 Project Structure
```
AI_UseCase/
├── app.py                    # Main Streamlit app
├── config/
│   └── config.py            # Configuration & API keys
├── models/
│   ├── llm.py               # LLM providers (Groq, OpenAI, Gemini)
│   └── embeddings.py        # Embedding model setup
├── utils/
│   ├── rag_utils.py         # Document loading, chunking, retrieval
│   ├── web_search.py        # Tavily web search integration
│   └── prompting.py         # System prompt builder
├── knowledge_base/          # Your local documents here
├── requirements.txt         # Python dependencies
├── run.py                   # Quick launcher
├── run.sh                   # Shell launcher
├── .env.local              # Environment variables
└── test_keys.py            # API key validation
```

## 🧪 Testing

Validate your setup:
```bash
python3 test_keys.py
```

This will verify both Groq and Tavily API keys are working.

## 🚪 Accessing the App

Once running, open your browser to:
```
http://localhost:8501
```

## ⚠️ Important Notes

- **Do NOT commit .env.local to public repositories** - it contains API keys
- Keep `knowledge_base/` documents clear of sensitive data
- Web search requires internet connectivity
- RAG indexing may take time with large documents

## 📝 Next Steps

1. **Add Documents**: Place files in `knowledge_base/` folder
2. **Test Features**: Enable/disable RAG and web search in sidebar
3. **Deploy**: Use Streamlit Cloud for production deployment
4. **Customize**: Modify system prompts and response modes in `/utils/prompting.py`

---

For deployment to Streamlit Cloud:
https://streamlit.io/cloud
