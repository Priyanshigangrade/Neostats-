#!/bin/bash
# Quick launcher for NeoStats AI Chatbot with API keys

cd "$(dirname "$0")"

echo "Loading API keys from .env.local..."
# Configure these in your environment:
# export GROQ_API_KEY='your_groq_key'
# export TAVILY_API_KEY='your_tavily_key'

echo "Starting NeoStats AI Chatbot..."
echo "Open: http://localhost:8501"
echo ""

python3 -m streamlit run app.py
