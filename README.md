# 🤖 Debales AI Assistant (LangGraph + RAG + SERP)

## 📌 Project Overview

This project is an AI-powered chatbot built using **LangGraph** that can answer:

- Debales AI related questions using **RAG (Retrieval-Augmented Generation)**
- General questions using a **SERP (Google Search API) tool**
- Mixed queries using both **RAG + SERP**
- Avoids hallucination when reliable information is not available

---

## 🚀 Features

- 🔍 Scrapes Debales AI website & blog content  
- 📚 Stores data in FAISS vector database  
- 🧠 Uses RAG for domain-specific answers  
- 🌐 Uses SERP API for external queries  
- 🔀 Smart routing using LangGraph  
- 🛑 No hallucination (returns safe fallback)  

---

## 🛠️ Tech Stack

- Python  
- LangGraph  
- LangChain  
- FAISS (Vector DB)  
- HuggingFace Embeddings  
- BeautifulSoup (Web Scraping)  
- SerpAPI (Search Tool)  
- Google Gemini API (LLM)  

---

## 🧩 Workflow
User Question
↓
Router (LangGraph)
↓
RAG / SERP / BOTH
↓
Final Answer Generation


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-link>
cd debales-ai-agent

2️⃣ Create virtual environment
python -m venv venv
Activate:
venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Set environment variables
Create a .env file:

GOOGLE_API_KEY=your_google_gemini_api_key

SERPAPI_API_KEY=your_serpapi_api_key

⚠️ Do NOT upload .env to GitHub

5️⃣ Run scraper
python scraper.py
This will create:
data/debales_docs.txt

6️⃣ Create vector database
python vector_store.py
This will create:
faiss_index/

7️⃣ Run chatbot
python app.py

💬 Example Queries
🔹 RAG (Debales AI)
What does Debales AI do?
🔹 SERP (General)
What is LangGraph?
🔹 BOTH (Mixed)
Compare Debales AI with latest AI automation trends.
🔹 Unknown
What is Debales AI revenue?
Output:
I could not find reliable information about this.

🔐 No Hallucination Rule
The chatbot strictly follows:


If information is not available in retrieved data or search results, it does NOT generate false answers.



📂 Project Structure
debales-ai-agent/│├── app.py├── scraper.py├── vector_store.py├── graph.py├── tools.py├── requirements.txt├── .env.example├── README.md└── data/

🧪 Routing Logic
Query TypeActionDebales relatedRAGGeneralSERPMixedRAG + SERP

📌 Notes


Ensure API keys are valid

Run scraper before vector store

Run vector store before chatbot

Internet connection required for SERP API



👩‍💻 Author
Tannu Gupta
B.Tech CSE | AI Enthusiast
🔗 GitHub: https://github.com/Tannugupta04/Debales-ai-agent/tree/main

