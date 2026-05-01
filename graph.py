import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from vector_store import load_vector_store
from tools import serp_search

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
vectorstore = load_vector_store()

class AgentState(TypedDict):
    question: str
    route: str
    rag_context: str
    serp_context: str
    final_answer: str

def router_node(state: AgentState):
    question = state["question"].lower()

    debales_keywords = [
        "debales",
        "debales ai",
        "company",
        "their product",
        "their service",
        "their services",
        "their integration",
        "their integrations",
        "website",
        "blog"
    ]

    mixed_keywords = [
        "compare",
        "latest",
        "trend",
        "trends",
        "market",
        "competitor",
        "vs",
        "versus"
    ]

    is_debales = any(keyword in question for keyword in debales_keywords)
    is_mixed = any(keyword in question for keyword in mixed_keywords)

    if is_debales and is_mixed:
        route = "BOTH"
    elif is_debales:
        route = "RAG"
    else:
        route = "SERP"

    return {"route": route}

def rag_node(state: AgentState):
    question = state["question"]

    docs = vectorstore.similarity_search(question, k=4)

    if not docs:
        context = "No relevant Debales AI context found."
    else:
        context = "\n\n".join([doc.page_content for doc in docs])

    return {"rag_context": context}

def serp_node(state: AgentState):
    question = state["question"]

    search_context = serp_search(question)

    return {"serp_context": search_context}

def answer_node(state: AgentState):
    question = state["question"]
    route = state["route"]
    rag_context = state.get("rag_context", "")
    serp_context = state.get("serp_context", "")

    prompt = f"""
You are a helpful AI assistant for Debales AI.

Your job:
- If the route is RAG, answer using Debales AI context only.
- If the route is SERP, answer using search results only.
- If the route is BOTH, combine Debales AI context and search results.
- Do not hallucinate.
- If reliable information is not available, clearly say:
  "I could not find reliable information about this."

Route:
{route}

User Question:
{question}

Debales AI Context:
{rag_context}

Search Results Context:
{serp_context}

Write a clear and helpful final answer.
"""

    response = llm.invoke(prompt)

    return {"final_answer": response.content}

def decide_after_router(state: AgentState):
    if state["route"] == "RAG":
        return "rag"
    elif state["route"] == "SERP":
        return "serp"
    elif state["route"] == "BOTH":
        return "rag"
    else:
        return "serp"

def decide_after_rag(state: AgentState):
    if state["route"] == "BOTH":
        return "serp"
    return "answer"

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("rag", rag_node)
workflow.add_node("serp", serp_node)
workflow.add_node("answer", answer_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    decide_after_router,
    {
        "rag": "rag",
        "serp": "serp"
    }
)

workflow.add_conditional_edges(
    "rag",
    decide_after_rag,
    {
        "serp": "serp",
        "answer": "answer"
    }
)

workflow.add_edge("serp", "answer")
workflow.add_edge("answer", END)

app_graph = workflow.compile()