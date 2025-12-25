import requests
from bs4 import BeautifulSoup
from tools.base import BaseTool, ToolResult
from config.settings import WEB_SEARCH_TIMEOUT

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the web and returns top search results"

    def run(self, **kwargs) -> ToolResult:
        query = kwargs.get("query")

        if not query:
            return ToolResult(
                success=False,
                error_type="permanent",
                error_message="No query provided"
            )

        try:
            response = requests.post(
                "https://duckduckgo.com/html/",
                data={"q": query},
                timeout=WEB_SEARCH_TIMEOUT
            )
            response.raise_for_status()
        except Exception as e:
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=f"Search request failed: {str(e)}"
            )

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            for result in soup.select(".result"):
                title = result.select_one(".result__title")
                snippet = result.select_one(".result__snippet")
                link = result.select_one(".result__a")

                if title and snippet and link:
                    results.append({
                        "title": title.get_text(strip=True),
                        "snippet": snippet.get_text(strip=True),
                        "url": link["href"],
                    })

            return ToolResult(
                success=True,
                output={
                    "query": query,
                    "results": results
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error_type="transient",
                error_message=f"Failed to parse search results: {str(e)}"
            )