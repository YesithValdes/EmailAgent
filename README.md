# 📧 Email Agent: Autonomous Inbox Manager

[![LangGraph](https://img.shields.io/badge/Powered%20by-LangGraph-blue)](https://langchain-ai.github.io/langgraph/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced autonomous email assistant built with **LangGraph** and **Next.js**. This agent doesn't just filter emails; it understands context, manages your calendar, and learns your preferences over time.

---

## 🌟 Key Features

- **Autonomous Triage**: Automatically classifies emails into `Respond`, `Ignore`, or `Notify`.
- **Human-in-the-Loop (HITL)**: Uses the **Agent Inbox** UI to pause and ask for your approval on critical actions (like sending emails or scheduling meetings).
- **Persistent Memory**: Remembers your writing style, response preferences, and triage rules across different conversations using LangGraph Store.
- **Gmail & Calendar Integration**: Full toolset for reading/sending emails and managing Google Calendar events.
- **Reusable Patterns**: Includes a set of "Skills" (documentation) to apply these patterns to other agentic projects.

---

## 🏗️ Architecture

The project follows a **Router-Worker** pattern:
1.  **Triage Router**: Analyzes incoming emails and decides the next step.
2.  **Response Agent**: A specialized sub-graph that handles drafting and tool execution.
3.  **Agent Inbox**: A modern web interface for real-time human interaction.

---

## 📂 Project Structure

```text
.
├── src/gmail_agent/       # Core Agent Logic (Python/LangGraph)
├── agent-inbox/           # Frontend UI (Next.js)
├── skills/                # Reusable design patterns & guides
├── run_dataset.py         # Evaluation pipeline
├── langgraph.json         # LangGraph Cloud configuration
└── .env.example           # Template for environment variables
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & Yarn/NPM
- Google Cloud Project with Gmail & Calendar API enabled
- Groq or OpenAI API Key

### 1. Setup Backend
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your keys:
- `GROQ_API_KEY`
- `LANGSMITH_API_KEY`
- Google OAuth credentials (`credentials.json`)

### 3. Setup Frontend
```bash
cd agent-inbox
npm install
npm run dev
```

---

## 📘 Reusable Skills

This repository contains a `skills/` directory with detailed guides on:
- [LangGraph Router-Worker Pattern](./skills/skill_langgraph_router_worker.md)
- [Human-in-the-Loop Interrupts](./skills/skill_hitl_interrupts.md)
- [Persistent Memory Store](./skills/skill_persistent_memory_store.md)
- [Agent Evaluation Datasets](./skills/skill_agent_evaluation_datasets.md)

---

## ☁️ Deployment

### Backend (LangGraph Cloud)
Deploy to **LangGraph Cloud** via LangSmith. Use the root directory for the deployment.

### Frontend (Agent Inbox)
Deploy to **Vercel**. Set the `Root Directory` to `agent-inbox/` in your Vercel project settings.

---

## 🤝 Contributing
Feel free to open issues or pull requests. For large changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
[MIT](LICENSE)
