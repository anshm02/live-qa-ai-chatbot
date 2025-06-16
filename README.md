# live-qa-ai-chatbot

# Live QA AI Chatbot (Backend)

This is the backend implementation of a real-time question-answering (QA) chatbot built using FastAPI and integrated with a vector database (Pinecone) and a large language model (LLM). The goal is to support live question answering from a given document or knowledge base using retrieval-augmented generation (RAG).

## Features

- FastAPI-based backend for scalable API endpoints
- Pinecone vector store for semantic document retrieval
- RAG architecture for accurate and context-aware answers
- Embedding-based similarity search to retrieve relevant context
- Easily extendable for frontend and chat integrations (e.g., React, Next.js)

## Getting Started

### Prerequisites

- Python 3.8+
- Pinecone API Key

### Installation

```bash
git clone https://github.com/anshm02/live-qa-ai-chatbot.git
cd live-qa-ai-chatbot
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
