# 📧 Email Agent — Autonomous Email Assistant with Local & Cloud LLMs

An autonomous email assistant built with **LangGraph** that reads, classifies, and responds to emails using a Human-in-the-Loop (HITL) approach. Designed to work both with **local SLMs (Small Language Models)** via Ollama and with cloud APIs (Google Gemini, Groq).

> **Educational Project** — Adapted to run with small local models to demonstrate autonomous agent architecture without cloud API costs.

---

## ✨ Features

- 🔍 **Automatic email triage** — classifies emails as `respond`, `notify`, or `ignore`
- ✍️ **AI-drafted replies** — the agent writes email responses for human approval
- 📅 **Calendar integration** — schedules meetings via Google Calendar
- 🧠 **Persistent memory** — learns your preferences over time (triage, response style, calendar habits)
- 🖥️ **Human-in-the-Loop UI** — review and approve agent actions via [Agent Inbox](https://github.com/langchain-ai/agent-inbox)
- 🔒 **100% local mode** — runs entirely on your machine with Ollama (no data leaves your computer)
- ☁️ **Cloud mode** — optionally use Google Gemini (free tier) or Groq API

---

## 🏗️ Architecture

```
Gmail API
    │
    ▼
┌─────────────────────────────────────┐
│           LangGraph Workflow         │
│                                     │
│  ┌──────────────┐                   │
│  │ Triage Router│ → ignore → END    │
│  └──────┬───────┘                   │
│         │ notify                    │
│         ▼                           │
│  ┌──────────────────┐               │
│  │ Triage Interrupt │ ◄──── Agent Inbox (UI)
│  └──────┬───────────┘               │
│         │ respond                   │
│         ▼                           │
│  ┌──────────────────┐               │
│  │  Response Agent  │ ◄──── Agent Inbox (UI)
│  │  (LLM + Tools)   │               │
│  └──────┬───────────┘               │
│         │                           │
│         ▼                           │
│    Mark as Read → END               │
└─────────────────────────────────────┘
         │
         ▼
   BaseStore (Memory)
   ├── triage_preferences
   ├── response_preferences
   └── cal_preferences
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM (local) | [Ollama](https://ollama.com) + Gemma / LLaMA 3 |
| LLM (cloud) | Google Gemini 2.0 Flash / Groq |
| Email & Calendar | Gmail API + Google Calendar API |
| Human-in-the-Loop UI | [Agent Inbox](https://github.com/langchain-ai/agent-inbox) (Next.js) |
| Memory | LangGraph `BaseStore` (persistent) + `MessagesState` (short-term) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

---

## 📋 Prerequisites

- Python **3.11 – 3.13**
- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- [Node.js](https://nodejs.org/) + npm — for the Agent Inbox UI
- [Ollama](https://ollama.com) — for local model inference (optional)
- A **Google account** with Gmail API enabled

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/EmailAgent.git
cd EmailAgent
```

### 2. Install Python dependencies

```bash
uv sync
```

### 3. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LangSmith (optional, for tracing)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=email-agent

# LLM APIs (choose one or both)
GOOGLE_API_KEY=your_google_api_key        # For Gemini (free tier available)
GROQ_API_KEY=your_groq_api_key            # For Groq (free tier available)

# Python path
PYTHONPATH=src
```

> **Using local models?** No API keys needed — just install Ollama and pull a model (see step 5).

### 4. Set up Gmail API

Follow the [Gmail API setup guide](./src/gmail_agent/tools/gmail/README.md) to:
1. Create a Google Cloud project
2. Enable the Gmail API and Google Calendar API
3. Download your `credentials.json`
4. Run the authentication script:

```bash
uv run python src/gmail_agent/tools/gmail/setup_gmail.py
```

### 5. Choose your LLM

Open `src/gmail_agent/email_agent.py` and uncomment the model you want to use:

```python
# ✅ Option A: Google Gemini (free tier — recommended for cloud)
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai", temperature=0.0)

# ✅ Option B: Local model via Ollama (100% private, no API key needed)
# llm = init_chat_model("gemma4:e2b", model_provider="ollama", temperature=0.0)

# ✅ Option C: Groq API (fast free inference)
# llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq", temperature=0.0)
```

**For Ollama**, first install and pull a model:

```bash
# Install Ollama from https://ollama.com
ollama pull gemma4:e2b
# or
ollama pull llama3.1
```

---

## 🚀 Running the Project

You need **two terminals** running simultaneously:

### Terminal 1 — Start the LangGraph agent server

```bash
uv run langgraph dev
```

This starts the agent API at `http://localhost:2024`.

### Terminal 2 — Start the Agent Inbox UI

```bash
cd agent-inbox
npm install
npm run dev
```

This starts the web interface at `http://localhost:3000`.

---

## 🔗 Connecting the UI to the Agent

1. Open `http://localhost:3000` in your browser
2. Click **Settings** → **Add Inbox**
3. Fill in the connection details:

| Field | Value |
|-------|-------|
| Deployment URL | `http://localhost:2024` |
| Assistant / Graph ID | `email_agent` |
| Name | `Email Assistant` (or any name you prefer) |

---

## 📬 Ingesting Emails

To process your Gmail emails, run the ingest script:

```bash
uv run python src/gmail_agent/tools/gmail/run_ingest.py \
  --email your@email.com \
  --minutes-since 60
```

This fetches emails from the last 60 minutes and runs them through the agent. Any emails requiring human input will appear in the Agent Inbox UI.

---

## 🧠 How Memory Works

The agent uses two types of memory:

| Type | Implementation | Duration |
|------|---------------|---------|
| **Short-term** | `MessagesState` (LangGraph) | Per email session |
| **Long-term** | `BaseStore` (LangGraph persistent store) | Across all sessions |

Long-term memory stores three profiles that are updated automatically based on your feedback:

- **Triage preferences** — which emails to respond to, notify about, or ignore
- **Response preferences** — your writing style and tone
- **Calendar preferences** — how you like meetings scheduled

---

## 📁 Project Structure

```
EmailAgent/
├── src/gmail_agent/
│   ├── email_agent.py        # Main LangGraph workflow
│   ├── schemas.py            # State, Router, and data models
│   ├── prompts.py            # System prompts
│   ├── utils.py              # Helper functions
│   └── tools/
│       ├── gmail/            # Gmail API integration & email ingestion
│       └── default/          # Email, calendar, and question tools
├── agent-inbox/              # Next.js Human-in-the-Loop UI
├── langgraph.json            # LangGraph deployment config
├── pyproject.toml            # Python dependencies
└── .env.example              # Environment variables template
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.

---

## 📄 License

This project is built on top of:
- [agent-inbox](https://github.com/langchain-ai/agent-inbox) — MIT License, Copyright (c) LangChain, Inc.

The email agent code is free to use for educational and personal projects.
