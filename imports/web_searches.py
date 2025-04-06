import requests
import pprint

def duckduckgo_search(query):
    res = requests.get("https://api.duckduckgo.com/", params={
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }).json()

    #pprint.pprint(res.get("RelatedTopics", None))
    
    # Try to get the direct abstract answer
    if res.get("AbstractText"):
        return res["AbstractText"]
    
    # Otherwise maybe there's a list of related topics
    if res.get("RelatedTopics"):
        results = []
        for topic in res["RelatedTopics"]:
            if "Text" in topic and "FirstURL" in topic:
                results.append(f"{topic['Text']} ({topic['FirstURL']})")
        return results[:5]  # Trim if too long
    else:
        return None

import duckduckgo_search as ddg_search
from googlesearch import search

def google_links(query, num=5):
    try:
        return list(search(query, num_results=num))
    except Exception as e:
        return [f"Error: {e}"]

import json
def smart_search(query):
    ddg_result = duckduckgo_search(query)
    if isinstance(ddg_result, list):
        return json.dumps({"source": "DuckDuckGo", "result": ddg_result})
    
    google_result = google_links(query)
    return json.dumps({"source": "Google", "result": google_result})



print(smart_search(input("?> ")))
