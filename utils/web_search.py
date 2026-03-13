from typing import List

from tavily import TavilyClient

from config.config import TAVILY_API_KEY


def search_web(query: str, max_results: int = 5) -> str:
    """Run live web search and return compact context text"""
    try:
        if not TAVILY_API_KEY:
            return ""

        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query, max_results=max_results)
        results: List[dict] = response.get("results", [])

        if not results:
            return ""

        compiled_snippets = []
        for item in results:
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            content = item.get("content", "")
            compiled_snippets.append(f"Title: {title}\nURL: {url}\nSnippet: {content}")

        return "\n\n".join(compiled_snippets)
    except Exception:
        return ""


def should_search_web(user_query: str, has_rag_context: bool) -> bool:
    """Heuristic to trigger web search for fresh or missing-knowledge queries"""
    try:
        query = user_query.lower()
        freshness_keywords = [
            "latest",
            "today",
            "current",
            "recent",
            "news",
            "update",
            "2025",
            "2026",
        ]
        has_freshness_intent = any(keyword in query for keyword in freshness_keywords)
        return has_freshness_intent or (not has_rag_context)
    except Exception:
        return False