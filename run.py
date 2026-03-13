#!/usr/bin/env python3
"""
NeoStats AI Chatbot - Quick Launcher
Reads API keys from environment and starts the Streamlit app
"""
import os
import subprocess
import sys

# API keys should be set in environment:
# export GROQ_API_KEY='your_groq_key'
# export TAVILY_API_KEY='your_tavily_key'
# Or in .env.local file

print("=" * 60)
print("NeoStats AI Chatbot - Launching")
print("=" * 60)

groq_key = os.environ.get('GROQ_API_KEY', '')
tavily_key = os.environ.get('TAVILY_API_KEY', '')

if groq_key:
    print("\n✅ Groq API Key: Configured")
else:
    print("\n⚠️  Groq API Key: Not set (set GROQ_API_KEY environment variable)")

if tavily_key:
    print("✅ Tavily API Key: Configured")
else:
    print("⚠️  Tavily API Key: Not set (optional, for web search)")

print("\n🌐 Open: http://localhost:8501")
print("=" * 60 + "\n")

# Start Streamlit app
try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
except KeyboardInterrupt:
    print("\n\nApp stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error starting app: {e}")
    sys.exit(1)
