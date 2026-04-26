---
title: Ask My PDF - AI ChatBot
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: streamlit
app_file: app.py
pinned: false
---

# 📄 Ask My PDF - AI ChatBot

A production-ready RAG (Retrieval-Augmented Generation) application built with Streamlit, LangChain, and ChromaDB.

## 🚀 Features
- **Multi-PDF Support**: Upload and process multiple documents at once.
- **Local LLM**: Uses `google/flan-t5-base` for inference (CPU friendly).
- **High-Quality Embeddings**: Powered by `sentence-transformers/all-mpnet-base-v2`.
- **Smart Retrieval**: Context-aware answering with relevance filtering.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **Vector Database**: ChromaDB
- **Models**: Hugging Face Transformers

## 📦 Deployment on HF Spaces
1. Create a new Space on Hugging Face.
2. Select **Streamlit** as the SDK.
3. Upload these files or push via Git.
4. The app will automatically build and deploy.
