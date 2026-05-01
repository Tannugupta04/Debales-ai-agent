import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

def serp_search(query):
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        return "SERPAPI_API_KEY is missing. Please add it in .env file."

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        organic_results = results.get("organic_results", [])

        if not organic_results:
            return "No reliable search results found."

        search_context = ""

        for result in organic_results[:5]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            link = result.get("link", "")

            search_context += f"Title: {title}\n"
            search_context += f"Snippet: {snippet}\n"
            search_context += f"Link: {link}\n\n"

        return search_context

    except Exception as e:
        return f"Search tool error: {e}"