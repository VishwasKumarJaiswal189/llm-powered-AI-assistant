# LLM-Powered Conversational AI Assistant

A production-ready, full-stack AI conversational assistant backend built with **FastAPI**, **LangChain**, and **OpenRouter**, featuring persistent conversational memory using **SQLite** and structured JSON output extraction.

## Features
- **Conversational Memory**: Multi-turn dialogue persistence powered by SQLite (`SQLChatMessageHistory`), retaining conversation context across server reboots.
- **Provider Agnostic**: Integrated with OpenRouter / OpenAI API specifications using LangChain.
- **Structured Output**: Dedicated endpoint parsing unstructured text into validated Pydantic schemas.
- **Interactive UI**: Embedded lightweight web chat interface served directly by FastAPI.
- **API Documentation**: Auto-generated interactive OpenAPI/Swagger docs at `/docs`.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI, Uvicorn
- **AI / LLM Orchestration**: LangChain, OpenRouter API
- **Data Validation & Schemas**: Pydantic v2
- **Persistence**: SQLite, SQLAlchemy
- **Environment Management**: python-dotenv, Codespaces Secrets

## Project Structure
```text
llm-powered-ai-assistant/
├── app/
│   ├── core/
│   │   └── config.py        # Settings and environment validation
│   ├── services/
│   │   ├── llm.py           # LangChain chains, prompts & structured output
│   │   └── memory.py        # SQLite chat history manager
│   └── main.py              # FastAPI endpoints and UI
├── data/                    # Persistent SQLite database (git-ignored)
├── tests/                   # Pytest test suite
├── requirements.txt
└── README.md