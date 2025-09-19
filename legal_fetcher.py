# legal_fetcher.py

import requests

GOOGLE_API_KEY = "AIzaSyDUMMY_KEY_1234567890abcdef"
SEARCH_ENGINE_ID = "dummy_search_engine_id_1234567890"

def get_legal_references(query):
    try:
        search_url = f"https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query + " site:indiankanoon.org OR site:legalserviceindia.com"
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        results_html = ""
        if "items" in data:
            for item in data["items"][:3]:
                title = item.get("title")
                link = item.get("link")
                snippet = item.get("snippet", "")
                results_html += f"🔹 [{title}]({link})\n\n> {snippet}\n\n"
        else:
            results_html = "⚠️ No legal documents found."

        return results_html
    except Exception as e:
        return f"⚠️ Legal Search Error: {e}"
