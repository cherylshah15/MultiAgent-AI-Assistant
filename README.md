# Multi-Agent AI Assistant

A cloud-deployed Multi-Agent AI system built with Streamlit, Groq, Pinecone, SQLite, and DuckDuckGo Search.

## Features

### Research Agent

Answers general AI and technical questions using Groq LLMs.

### Web Agent

Retrieves recent news and current information using DuckDuckGo Search.

### Database Agent

Queries a structured employee database using SQLite.

### RAG Agent

Uses Pinecone vector search and embeddings to answer questions from uploaded PDF documents.

## Architecture

User Query
↓
Router Agent
↓
├── Research Agent
├── Web Agent
├── Database Agent
└── RAG Agent

## Tech Stack

* Python
* Streamlit
* Groq API
* Pinecone Vector Database
* Sentence Transformers
* SQLite
* DuckDuckGo Search (DDGS)
* GitHub
* Streamlit Cloud

## Deployment

Live Application:

https://multiagent-ai-assistant-mzhshctvueywiatlbfvikc.streamlit.app/

## Example Queries

Research:

* What is machine learning?

Web:

* Latest AI news

Database:

* Who works in Finance?

RAG:

* Summarize the document

## Author

Cheryl Shah
