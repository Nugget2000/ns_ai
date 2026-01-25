"""
Modern Web Scraper using Playwright

A production-ready scraper that handles JavaScript-rendered content,
concurrent page processing, and intelligent content extraction.
"""

import os
import asyncio
import time
import logging
import re
import sys
from typing import Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass, field

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from google import genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SiteStats:
    """Statistics for a scraped site."""
    url: str
    pages_scraped: int = 0
    chars_saved: int = 0
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "pages_scraped": self.pages_scraped,
            "chars_saved": self.chars_saved,
            "errors": self.errors
        }


@dataclass
class ScrapeConfig:
    """Configuration for the scraper."""
    max_concurrent_pages: int = 5
    page_timeout_ms: int = 30000
    navigation_timeout_ms: int = 15000
    delay_between_requests: float = 0.2
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    excluded_extensions: tuple = ('.pdf', '.zip', '.exe', '.dmg', '.pkg', '.tar.gz')
    excluded_patterns: tuple = ('#', 'mailto:', 'tel:', 'javascript:')


def load_env() -> bool:
    """Load .env file to ensure GEMINI_API_KEY is available."""
    env_paths = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.getcwd(), "backend", ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "backend", ".env")
    ]

    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            if line.startswith("export "):
                                line = line[7:].strip()
                            if "=" in line:
                                key, value = line.split("=", 1)
                                os.environ[key.strip()] = value.strip().strip('"').strip("'")
                logger.info(f"Loaded environment variables from {env_path}")
                return True
            except Exception as e:
                logger.error(f"Error loading {env_path}: {e}")
    return False


# Load environment variables at module import
load_env()


class ContentExtractor:
    """Extracts and cleans text content from HTML pages."""

    # Site-specific selectors for main content areas
    SITE_SELECTORS = {
        "loopnlearn.org": {
            "main_selector": "#et-main-area",
            "remove_selectors": ["#main-footer", "nav", ".sidebar"]
        },
        "loopkit.github.io": {
            "main_selector": ".md-content",
            "remove_selectors": [".md-sidebar", ".md-header", ".md-footer"]
        }
    }

    @classmethod
    async def extract_text(cls, page: Page, url: str) -> str:
        """Extract clean text content from a page."""
        domain = urlparse(url).netloc

        # Find site-specific config
        site_config = None
        for site_domain, config in cls.SITE_SELECTORS.items():
            if site_domain in domain:
                site_config = config
                break

        # Remove unwanted elements
        await page.evaluate("""
            () => {
                const removeSelectors = ['script', 'style', 'noscript', 'iframe'];
                removeSelectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => el.remove());
                });
            }
        """)

        # Remove site-specific elements
        if site_config and site_config.get("remove_selectors"):
            for selector in site_config["remove_selectors"]:
                try:
                    await page.evaluate(f"""
                        () => {{
                            document.querySelectorAll('{selector}').forEach(el => el.remove());
                        }}
                    """)
                except Exception:
                    pass  # Selector might not exist on page

        # Get main content area or full body
        content_element = None
        if site_config and site_config.get("main_selector"):
            try:
                content_element = await page.query_selector(site_config["main_selector"])
            except Exception:
                pass

        if content_element:
            text = await content_element.inner_text()
        else:
            text = await page.inner_text("body")

        # Clean up the text
        return cls._clean_text(text)

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text."""
        # Split into lines and clean each
        lines = text.splitlines()
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if line:
                # Collapse multiple spaces
                line = re.sub(r'\s+', ' ', line)
                cleaned_lines.append(line)

        # Remove duplicate consecutive lines
        result_lines = []
        prev_line = None
        for line in cleaned_lines:
            if line != prev_line:
                result_lines.append(line)
                prev_line = line

        return '\n'.join(result_lines)


class ScraperService:
    """
    Modern async web scraper using Playwright.
    
    Handles JavaScript-rendered content, respects rate limits,
    and provides intelligent content extraction.
    """

    def __init__(
        self,
        cache_dir: str = "backend/cache",
        prompt_file: str = "backend/emanuel_prompt.txt",
        config: Optional[ScrapeConfig] = None
    ):
        self.cache_dir = cache_dir
        self.prompt_file = prompt_file
        self.config = config or ScrapeConfig()
        self.visited_urls: set[str] = set()
        self._semaphore: Optional[asyncio.Semaphore] = None

        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)

        # Initialize Gemini Client
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_client = None
        if self.api_key:
            self.gemini_client = genai.Client(api_key=self.api_key)
        else:
            logger.warning("GEMINI_API_KEY not set, will not be able to update file search store.")

    def _is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL is valid and belongs to base domain."""
        parsed = urlparse(url)

        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False

        # Must belong to the same domain
        if base_domain not in parsed.netloc:
            return False

        # Check excluded extensions
        lower_path = parsed.path.lower()
        for ext in self.config.excluded_extensions:
            if lower_path.endswith(ext):
                return False

        return True

    def _normalize_url(self, url: str) -> str:
        """Normalize URL by removing fragments and trailing slashes."""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        # Remove trailing slash for consistency (except for root)
        if normalized.endswith('/') and len(parsed.path) > 1:
            normalized = normalized[:-1]
        return normalized

    async def _extract_links(self, page: Page, base_url: str) -> set[str]:
        """Extract all valid links from a page."""
        domain = urlparse(base_url).netloc
        urls = set()

        try:
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a[href]'))
                    .map(a => a.href)
                    .filter(href => href && !href.startsWith('javascript:'))
            """)

            for href in links:
                # Skip excluded patterns
                if any(pattern in href for pattern in self.config.excluded_patterns):
                    continue

                # Normalize and validate
                normalized = self._normalize_url(href)
                if self._is_valid_url(normalized, domain) and normalized not in self.visited_urls:
                    urls.add(normalized)

        except Exception as e:
            logger.warning(f"Error extracting links from {base_url}: {e}")

        return urls

    async def _scrape_page(
        self,
        context: BrowserContext,
        url: str,
        domain: str
    ) -> tuple[Optional[str], set[str]]:
        """
        Scrape a single page and extract content and links.
        
        Returns: (extracted_text, new_links)
        """
        async with self._semaphore:
            page = await context.new_page()
            try:
                logger.info(f"Scraping: {url}")

                # Navigate with timeout
                await page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=self.config.navigation_timeout_ms
                )

                # Wait a bit for any lazy-loaded content
                await asyncio.sleep(0.5)

                # Extract text content
                text = await ContentExtractor.extract_text(page, url)

                # Extract links for further crawling
                new_links = await self._extract_links(page, url)

                return text, new_links

            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                return None, set()

            finally:
                await page.close()

    def _save_to_cache(self, url: str, text: str) -> int:
        """Save extracted text to cache file. Returns chars saved."""
        # Create safe filename
        safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + ".txt"
        filepath = os.path.join(self.cache_dir, safe_filename)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        content = f"URL: {url}\nExtraction Time: {timestamp}\n{'-' * 20}\n{text}"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return len(content)

    async def scrape_site(self, browser: Browser, start_url: str) -> SiteStats:
        """Crawl and scrape an entire site starting from start_url."""
        logger.info(f"Starting scrape for {start_url}")
        
        stats = SiteStats(url=start_url)
        domain = urlparse(start_url).netloc
        
        # Initialize semaphore for this scrape
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_pages)
        
        # Create browser context with custom user agent
        context = await browser.new_context(
            user_agent=self.config.user_agent,
            viewport={"width": 1920, "height": 1080}
        )

        try:
            urls_to_visit = {self._normalize_url(start_url)}

            while urls_to_visit:
                # Get batch of URLs to process
                batch = set()
                while urls_to_visit and len(batch) < self.config.max_concurrent_pages:
                    url = urls_to_visit.pop()
                    if url not in self.visited_urls:
                        batch.add(url)
                        self.visited_urls.add(url)

                if not batch:
                    break

                # Process batch concurrently
                tasks = [
                    self._scrape_page(context, url, domain)
                    for url in batch
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Process results
                for url, result in zip(batch, results):
                    if isinstance(result, Exception):
                        stats.errors.append(f"{url}: {str(result)}")
                        continue

                    text, new_links = result
                    if text:
                        chars = self._save_to_cache(url, text)
                        stats.pages_scraped += 1
                        stats.chars_saved += chars

                        # Add new links to queue
                        urls_to_visit.update(new_links - self.visited_urls)

                # Rate limiting delay
                await asyncio.sleep(self.config.delay_between_requests)

        finally:
            await context.close()

        return stats

    def compile_prompt(self) -> None:
        """Compile all cached files into the prompt file and save to Firestore."""
        logger.info("Compiling prompt file...")

        full_prompt = (
            "You are Emanuel, an AI assistant for the Nightscout and Loop community.\n"
            "Explicitly only answer using the information in the following context.\n"
            "Always answer with clickable links and clear instructions.\n"
            "If the answer is not in the context, state that you don't know based on the available information.\n\n"
            "=== CONTEXT START ===\n\n"
        )

        for filename in sorted(os.listdir(self.cache_dir)):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.cache_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        full_prompt += infile.read()
                        full_prompt += "\n\n" + "=" * 40 + "\n\n"
                except Exception as e:
                    logger.warning(f"Error reading cache file {filename}: {e}")

        full_prompt += "=== CONTEXT END ===\n"

        # Save to file
        with open(self.prompt_file, "w", encoding="utf-8") as outfile:
            outfile.write(full_prompt)
        logger.info(f"Prompt file created at {self.prompt_file} ({len(full_prompt):,} chars)")

        # Save to Firestore
        self._save_to_firestore(full_prompt)

    def _save_to_firestore(self, prompt: str) -> None:
        """Save prompt to Firestore if within size limits."""
        try:
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            if backend_dir not in sys.path:
                sys.path.append(backend_dir)

            try:
                from app.services.firebase import save_emanuel_prompt
            except ImportError:
                from services.firebase import save_emanuel_prompt

            if len(prompt.encode('utf-8')) > 1048000:
                logger.warning("Prompt exceeds Firestore 1MB limit. Skipping Firestore save.")
            else:
                save_emanuel_prompt(prompt)
                logger.info("Prompt saved to Firestore")

        except Exception as e:
            logger.error(f"Failed to save to Firestore: {e}")

    def update_gemini_store(self) -> None:
        """Upload compiled prompt to Gemini file search store."""
        if not self.gemini_client:
            logger.error("Gemini client not initialized. Cannot update file store.")
            return

        store_name = 'emanuel_scrape_store'
        logger.info(f"Updating Gemini file search store: {store_name}")

        try:
            # Find existing store
            file_search_stores = self.gemini_client.file_search_stores.list()
            file_search_store = None
            for store in file_search_stores:
                if store.display_name == store_name:
                    file_search_store = store
                    break

            # Delete existing store to ensure fresh data
            if file_search_store:
                logger.info(f"Deleting old store to ensure fresh data")
                self.gemini_client.file_search_stores.delete(
                    name=file_search_store.name,
                    config={"force": True}
                )

            # Create new store
            logger.info(f"Creating new file search store: {store_name}")
            file_search_store = self.gemini_client.file_search_stores.create(
                config={'display_name': store_name}
            )

            # Upload prompt file
            logger.info(f"Uploading {self.prompt_file} to Gemini...")
            operation = self.gemini_client.file_search_stores.upload_to_file_search_store(
                file=self.prompt_file,
                file_search_store_name=file_search_store.name,
                config={'display_name': 'emanuel_prompt'}
            )

            # Wait for upload to complete
            while not operation.done:
                logger.info("Uploading file to Gemini...")
                time.sleep(2)
                operation = self.gemini_client.operations.get(operation)

            logger.info("Gemini file search store updated successfully.")

        except Exception as e:
            logger.error(f"Error updating Gemini file search store: {e}")
            import traceback
            logger.error(traceback.format_exc())

    async def _run_async(self, sites: list[str]) -> dict:
        """Async implementation of the scraping workflow."""
        summary = {
            "sites_scraped": [],
            "total_pages": 0,
            "total_chars_saved": 0,
            "time_taken_seconds": 0
        }

        async with async_playwright() as p:
            # Launch browser (chromium for best compatibility)
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )

            try:
                for site in sites:
                    stats = await self.scrape_site(browser, site)
                    summary["sites_scraped"].append(stats.to_dict())
                    summary["total_pages"] += stats.pages_scraped
                    summary["total_chars_saved"] += stats.chars_saved

            finally:
                await browser.close()

        return summary

    def run(self) -> dict:
        """
        Main entry point - run the scraping and compilation workflow.
        
        Returns a summary of the operation.
        """
        start_time = time.time()

        sites = [
            "https://www.loopnlearn.org/",
            "https://loopkit.github.io/loopdocs/",
        ]

        # Run async scraping
        summary = asyncio.run(self._run_async(sites))

        # Compile prompt and update stores
        self.compile_prompt()
        self.update_gemini_store()

        end_time = time.time()
        summary["time_taken_seconds"] = round(end_time - start_time, 2)

        logger.info(
            f"Scraping complete: {summary['total_pages']} pages, "
            f"{summary['total_chars_saved']:,} chars in {summary['time_taken_seconds']}s"
        )

        return summary


# Convenience function for sync contexts
def run_scraper(
    cache_dir: str = "backend/cache",
    prompt_file: str = "backend/emanuel_prompt.txt"
) -> dict:
    """Run the scraper with specified configuration."""
    scraper = ScraperService(cache_dir=cache_dir, prompt_file=prompt_file)
    return scraper.run()


if __name__ == "__main__":
    # Detect working directory and adjust paths
    cwd = os.getcwd()
    if cwd.endswith("backend"):
        cache_dir = "cache"
        prompt_file = "emanuel_prompt.txt"
    else:
        cache_dir = "backend/cache"
        prompt_file = "backend/emanuel_prompt.txt"

    result = run_scraper(cache_dir=cache_dir, prompt_file=prompt_file)
    print(f"\n{'='*50}")
    print("Scraping Summary:")
    print(f"  Sites: {len(result['sites_scraped'])}")
    print(f"  Pages: {result['total_pages']}")
    print(f"  Characters: {result['total_chars_saved']:,}")
    print(f"  Time: {result['time_taken_seconds']}s")
    print(f"{'='*50}")
