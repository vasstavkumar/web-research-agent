import os
import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
import requests
from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import List, Dict


load_dotenv()

mcp = FastMCP("web_research_tools")

@mcp.tool()
def web_search_tool(search_query):

    """
    Performs a web search using the SerpAPI and returns a list.

    Args:
        search_query (str): The search query string to search.

    Returns:
        list which has a dictionary which contains links and snippets
    
    """

    params = {
        "engine": "google",
        "q": search_query,
        "api_key": os.getenv('SERP_API_KEY')
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    urls = [result["link"] for result in organic_results if "link" in result]
    
    # result = [{"link": result["link"], "snippet": result["snippet"]} for result in organic_results if "link" in result]
    
    return urls

@mcp.tool()
def web_scraping_tool(url_list: List[str]) -> List[Dict[str, str]]:
    """
    Scrapes visible text content from a list of URLs.

    Args:
        url_lis (List[str]): List of webpage URLs.

    Returns:
        List[str]: List of string containing the context of the web-pages.
    """

    context = []

    process_urls = url_list[:3]

    for url in process_urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            context.append(text)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Could not fetch {url} — {e}")
            continue

        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while scraping {url} — {e}")
            continue

    return context

@mcp.tool()
def news_aggregrator(search_query):
    """
    Performs a Google News search for the given query and returns a list of news article URLs.

    Args:
        search_query (str): The query to search for in Google News.

    Returns:
        List[str]: A list of URLs from the top news articles related to the search query. 
                   Returns an empty list if no results are found.              
    """
    params = {
        "engine": "google_news",
        "q": search_query,
        "api_key": os.getenv('SERP_API_KEY'),
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "news_results" in results:
        news_results = results["news_results"]
        
        urls = [result["link"] for result in news_results if "link" in result]
        
        return urls[:3]
    else:
        return []

if __name__ == "__main__":
    mcp.run(transport="stdio")

