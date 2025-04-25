# Web Research Agent

## Overview

The **Web Research Agent** is an intelligent Agent designed to analyze user queries, uses the MCP(model context protocol), select the appropriate web research tools, collect reliable information from various web sources, and synthesize it into a well-structured and fact-based summary. The agent works like a responsible human researcher, gathering information from trusted sources and providing accurate, concise answers.

---

## Features

- **Query Analysis**: The agent can determine the intent behind a user query (news-related or general research).
- **Tool Integration**: The agent uses various tools to gather data:
  - **news_aggregrator** for news-related queries (e.g., current events, trending topics).
  - **web_search_tool** for general or non-news queries.
  - **web_scraping_tool** to fetch full page content from selected URLs.
- **Synthesis**: The agent generates concise summaries by combining information from multiple sources, resolving contradictions, and organizing data logically.
- **Error Handling**: The agent handles errors gracefully, ensuring no crashes due to broken or empty pages.
- **Citations**: The agent provides citations where necessary, referencing URLs or page titles.

---

## Tools Used

1. **news_aggregrator(query: str)**  
   - Use this tool for retrieving recent news articles related to a user’s query.
   - Returns a list of URLs of news articles.

2. **web_search_tool(query: str)**  
   - Use this tool for general-purpose research or non-news queries.
   - Returns a list of results with links (without snippets).

3. **web_scraping_tool(urls: List[str])**  
   - This is the tool used to fetch full-page content from a list of URLs. It is the only valid data source for generating answers.

---

## How It Works

### 1. **Query Analysis**
   The agent first analyzes the user’s query to determine its intent:
   - If the query is news-related, it uses **news_aggregrator** to gather recent articles.
   - For all other queries, it uses **web_search_tool** to find relevant sources.

### 2. **Extract URLs**
   The agent extracts URLs from the results of the selected tool.

### 3. **Web Scraping**
   The agent uses **web_scraping_tool** to fetch the full content from the URLs and gather the necessary data.

### 4. **Information Synthesis**
   The agent synthesizes the data from multiple sources, resolves contradictions, organizes the content, and generates a clear, concise, and factually correct summary.

---

```bash
git clone https://github.com/vasstavkumar/web-research-agent.git
cd web-research-agent


