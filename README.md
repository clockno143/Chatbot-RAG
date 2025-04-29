# 🤖 LEXI — AI-Powered Immigration Law Chatbot

**LEXI** is a full-stack chatbot system built using **Retrieval-Augmented Generation (RAG)**, combining **Azure AI Search (Vector DB)** with **OpenAI GPT-4 Turbo**, and featuring a clean **React-based frontend**. It helps users find accurate answers to questions about **U.S. immigration law**, backed by real documents and citations.

---

## 🔍 What LEXI Does

LEXI enables users to ask natural-language questions related to immigration. It:

- Uses **Azure AI Search with vector embeddings** to retrieve relevant documents
- Feeds the context to **OpenAI GPT-4 Turbo** to generate answers
- Displays answers + reference sources in a clean **React UI**

---

## 🧠 Tech Stack

| Component       | Technology                        |
|----------------|------------------------------------|
| Language Model | OpenAI GPT-4 Turbo                 |
| Vector Search  | Azure AI Search (Vector DB)        |
| Backend API    | FastAPI (Python)                   |
| Frontend UI    | React.js                           |
| Secrets Mgmt   | `.env` + `os.getenv()`             |
| Hosting/Infra  | Azure (Search, App Service, etc.)  |

---


