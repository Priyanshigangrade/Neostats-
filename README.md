# NeoStats AI Chatbot - The Blueprint

An intelligent, context-aware chatbot with **RAG (Retrieval-Augmented Generation)**, **live web search**, and **adaptive response modes**.

## 🎯 Project Overview

This chatbot solution implements three core capabilities to create a comprehensive conversational AI system:

1. **RAG Integration** - Retrieves relevant context from local documents
2. **Live Web Search** - Fetches real-time information when needed
3. **Response Modes** - Toggle between concise summaries and detailed explanations

## ✨ Features

### 💬 Multi-Provider LLM Support
- **Groq** (Default - Fast & efficient)
- **OpenAI** (GPT-4o, GPT-4o-mini)
- **Google Gemini** (gemini-1.5-pro, gemini-1.5-flash)

### 📚 RAG (Retrieval-Augmented Generation)
- Load local documents (`.txt`, `.md`, `.pdf`, `.csv`, `.json`)
- Vector embeddings using HuggingFace models
- Chroma vector database for fast retrieval
- One-click RAG index rebuild

### 🌐 Live Web Search
- Tavily API integration
- Smart triggering for freshness queries
- Automatic fallback when local context is insufficient

### ⚙️ Response Modes
- **Concise Mode**: Short, summarized answers (3-6 lines)
- **Detailed Mode**: Thorough explanations with context and caveats

### 🎨 UI/UX
- Clean Streamlit interface
- Real-time chat with history
- Response context transparency
- Settings sidebar for easy configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip/pip3

### Installation

```bash
# Clone the repository
git clone https://github.com/Priyanshigangrade/Neostats-.git
cd AI_UseCase

# Install dependencies
pip install -r requirements.txt

# Set API keys
export GROQ_API_KEY='your_groq_key'
export TAVILY_API_KEY='your_tavily_key'

# Run the app
python3 run.py
```

Or use the one-liner:
```bash
./run.sh
```

The app will be available at: **http://localhost:8501**

## 📁 Project Structure

```
AI_UseCase/
├── app.py                      # Main Streamlit application
├── config/
│   └── config.py              # Configuration & environment variables
├── models/
│   ├── llm.py                 # Multi-provider LLM factory
│   └── embeddings.py          # Embedding model setup
├── utils/
│   ├── rag_utils.py           # Document loading & retrieval
│   ├── web_search.py          # Live web search integration
│   └── prompting.py           # System prompt builder
├── knowledge_base/            # Your local documents here
├── requirements.txt           # Dependencies
├── run.py & run.sh           # Quick launchers
└── .env.local                # Local environment variables (not committed)
```

## 🔑 Getting API Keys

### Groq
1. Visit https://console.groq.com/keys
2. Create an API key
3. Set: `export GROQ_API_KEY='your_key'`

### Tavily (Web Search)
1. Visit https://app.tavily.com/
2. Create API key
3. Set: `export TAVILY_API_KEY='your_key'`

### OpenAI / Google Gemini
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://aistudio.google.com/app/apikey

## 📚 Using RAG

1. **Add documents** to `knowledge_base/` folder
2. In app sidebar, click **"Rebuild RAG Index"**
3. Ask questions - the chatbot will reference your documents

Supported formats: `.txt`, `.md`, `.pdf`, `.csv`, `.json`

## 🎮 Usage Examples

### Concise Mode
- Good for quick facts and summaries
- Perfect for mobile or time-sensitive queries

### Detailed Mode
- Comprehensive explanations with examples
- Best for learning and research

### RAG + Web Search
- Combines local knowledge with real-time information
- Automatically triggered based on query freshness indicators

## 🛠️ Technology Stack

- **Framework**: Streamlit
- **LLM Integration**: LangChain
- **Embeddings**: HuggingFace Transformers
- **Vector Storage**: Chroma
- **Web Search**: Tavily API
- **Language**: Python 3.9+

## 📝 Configuration

Edit `config/config.py` to customize:

```python
CHUNK_SIZE = 1000          # Document chunk size
CHUNK_OVERLAP = 150        # Overlap between chunks
TOP_K = 4                  # Number of retrieved chunks
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
```

## 🚨 Error Handling

All functions include comprehensive try-catch blocks:
- Graceful degradation on API failures
- Informative error messages
- Automatic fallback mechanisms

## 📊 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect at https://streamlit.io/cloud
3. Add secrets in Streamlit settings:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`

### Docker
```bash
docker build -t neostats-chatbot .
docker run -p 8501:8501 -e GROQ_API_KEY='...' neostats-chatbot
```

## 👤 Author

**Priyanshi Gangrade**
- Email: priyanshigangrade25@gmail.com
- GitHub: [@Priyanshigangrade](https://github.com/Priyanshigangrade)

## 📄 License

MIT License - Feel free to use this project for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: priyanshigangrade25@gmail.com

## 🎓 Learning Resources

- [LangChain Documentation](https://docs.langchain.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Chroma Vector DB](https://docs.trychroma.com)
- [Tavily Web Search API](https://tavily.com)

---

**Built with ❤️ by Priyanshi Gangrade**
