import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse


class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            #Bug Fix: Added headers and timeout to avoid 403 errors and hanging requests
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            #Bug Fix: Store page text correctly in index
            self.index[url] = soup.get_text()

            #Bug Fix: Use base_url to limit crawling to internal domain only

            base_url = base_url or url
            parsed_base = urlparse(base_url)

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    joined_url = urljoin(base_url, href)
                    parsed_href = urlparse(joined_url)

                    #Bug Fix: Only follow internal links (same domain or relative)
                    if parsed_href.netloc == '' or parsed_href.netloc == parsed_base.netloc:
                        self.crawl(joined_url, base_url)
        except Exception as e:
            #Bug Fix: Added error handling so the crawler doesn’t crash
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            #Bug Fix: Corrected search logic to add URL if keyword is found
            if keyword.lower() in text.lower():
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                #Bug Fix: Used correct variable `result` instead of undefined `undefined_variable`
                print(f"- {result}")
        else:
            print("No results found.")


def main():
    crawler = WebCrawler()
    start_url = "https://example.com"

    #Bug Fix: Typo fixed — was `crawler.craw()` before
    crawler.crawl(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)


# ===================== Unit Tests ======================

import unittest
from unittest.mock import patch, MagicMock


class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Bug Fix: Assert that internal link "/about" is visited
        self.assertIn("https://example.com/about", crawler.visited)
        self.assertIn("https://example.com", crawler.index)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

         # Bug Fix: Ensure URL is marked as visited even on error
        self.assertIn("https://example.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No key here"

         # Bug Fix: Test correct search logic — only include matching pages
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        # Bug Fix: Actually test printed output
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        mock_stdout.write.assert_any_call("Search results:\n")
        mock_stdout.write.assert_any_call("- https://test.com/result\n")


# =================== Run both main and tests ===================
if __name__ == "__main__":
    unittest.main(exit=False)
    print("\n--- Running Web Crawler ---")
    main()
