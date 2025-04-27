import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from duckduckgo_search import DDGS

class ResearchAgent:
    """
    ResearchAgent performs web searches and scrapes content for a given company.
    It uses DuckDuckGo search to find relevant links, then requests+BeautifulSoup
    to fetch and parse pages, and crawls internally up to 2 levels for more info.
    """

    def __init__(self):
        # Define a common headers dict with a User-Agent to mimic a browser.
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.36"
            )
        }

    def search(self, query: str, max_results: int = 5):
        """
        Perform a web search for the given query using DuckDuckGo.
        Returns a list of result dicts with keys 'title', 'href', etc.
        """
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=max_results)
        except Exception as e:
            print(f"Search failed for query '{query}': {e}")
            return []
        return results or []

    def fetch_page(self, url: str):
        """
        Fetch a page URL and return a BeautifulSoup object of its HTML.
        Returns None if the request fails or content is not HTML.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # raise HTTPError for bad status
        except requests.RequestException as e:
            print(f"Request failed for URL '{url}': {e}")
            return None

        # Only proceed if the content type is HTML
        content_type = response.headers.get("Content-Type", "")
        if "html" not in content_type:
            print(f"Skipping non-HTML content at '{url}' (Content-Type: {content_type})")
            return None

        # Parse and return the BeautifulSoup object
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def extract_text(self, soup: BeautifulSoup):
        """
        Extract and concatenate text from the parsed HTML soup.
        We pull text from <h1>, <h2>, <h3>, and <p> tags for relevance.
        """
        texts = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
            content = tag.get_text().strip()
            # Only include non-empty and reasonably long text
            if content and len(content) > 20:
                texts.append(content)
        return "\n".join(texts)

    def crawl_site(self, base_url: str, max_depth: int = 1):
        """
        Crawl the given base URL up to max_depth levels of internal links.
        Returns the concatenated text content from all visited pages.
        Only follows links on the same domain and avoids irrelevant pages.
        """
        parsed = urlparse(base_url)
        base_domain = parsed.netloc
        visited = set()
        content_parts = []

        queue = [(base_url, 0)]
        while queue:
            url, depth = queue.pop(0)
            if url in visited or depth > max_depth:
                continue
            visited.add(url)

            soup = self.fetch_page(url)
            if soup is None:
                continue

            # Extract and accumulate text content from this page
            page_text = self.extract_text(soup)
            content_parts.append(f"Content from {url}:\n{page_text}\n")

            # If we haven't reached max depth, enqueue relevant internal links
            if depth < max_depth:
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    full_url = urljoin(base_url, href)
                    parsed_href = urlparse(full_url)

                    # Ensure it's the same domain (no external links)
                    if parsed_href.netloc != base_domain:
                        continue
                    # Skip if already visited or pointing to a fragment or script
                    if full_url in visited or full_url.startswith('#'):
                        continue

                    href_lower = full_url.lower()
                    text_lower = (a.get_text() or "").lower()

                    # Skip common irrelevant or sensitive links
                    if any(kw in href_lower for kw in [
                        '.pdf', '.jpg', '.jpeg', '.png', '.gif', 'mailto:', 'javascript:'
                    ]):
                        continue
                    if any(kw in href_lower for kw in [
                        'login', 'signup', 'register', 'job', 'career', 'privacy', 'terms', 'subscribe', 'contact'
                    ]):
                        continue

                    # Only follow links that likely contain relevant info
                    include_keywords = [
                        'about', 'team', 'history', 'company', 'leadership',
                        'product', 'service', 'news', 'press', 'blog'
                    ]
                    if any(kw in href_lower or kw in text_lower for kw in include_keywords):
                        queue.append((full_url, depth + 1))

        return "\n".join(content_parts)

    def get_company_info(self, company_name: str):
        """
        High-level method to search for a company and gather information.
        Returns a dict with scraped text from the company website and Wikipedia.
        """
        results = self.search(company_name, max_results=10)
        info = {}

        # Find Wikipedia link if present
        wiki_url = None
        for result in results:
            href = result.get('href', '')
            if href and 'wikipedia.org' in href.lower():
                wiki_url = href
                break

        # Find first non-Wikipedia link (likely the official site)
        official_url = None
        for result in results:
            href = result.get('href', '')
            if href and 'wikipedia.org' not in href.lower():
                official_url = href
                break

        # Scrape Wikipedia content
        if wiki_url:
            soup = self.fetch_page(wiki_url)
            if soup:
                text = self.extract_text(soup)
                info['wikipedia'] = text[:5000]

        # Scrape the official site (and internal links up to depth 1 or 2)
        if official_url:
            official_soup = self.fetch_page(official_url)
            if official_soup:
                # Combine main page content
                main_text = self.extract_text(official_soup)
                # Crawl one level deep for more content
                internal_text = self.crawl_site(official_url, max_depth=1)
                combined = f"{main_text}\n\n{internal_text}"
                info['website'] = combined[:5000]

        return info