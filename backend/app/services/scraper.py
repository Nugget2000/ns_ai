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
import json
import unicodedata
from typing import Optional
from urllib.parse import urlparse
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


_UNICODE_REPLACEMENTS = str.maketrans({
    "\u00a0": " ",   # non-breaking space
    "\u200b": "",    # zero-width space
    "\u200c": "",    # zero-width non-joiner
    "\u200d": "",    # zero-width joiner
    "\ufeff": "",    # BOM / zero-width no-break space
    "\u2018": "'",   # left single quotation mark
    "\u2019": "'",   # right single quotation mark
    "\u201c": '"',   # left double quotation mark
    "\u201d": '"',   # right double quotation mark
    "\u2013": "-",   # en dash
    "\u2014": "--",  # em dash
    "\u2026": "...", # ellipsis
    "\u00ad": "",    # soft hyphen
})


def _clean_unicode(text: str) -> str:
    """Normalize Unicode and replace ambiguous characters with ASCII equivalents."""
    text = unicodedata.normalize("NFKC", text)
    return text.translate(_UNICODE_REPLACEMENTS)


def load_env() -> bool:
    """Load .env file to ensure GEMINI_API_KEY is available."""
    # This file lives at backend/app/services/scraper.py — three levels up is the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_paths = [
        os.path.join(project_root, ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]

    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        if line.startswith("export "):
                            line = line[7:].strip()
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
        config: Optional[ScrapeConfig] = None
    ):
        self.cache_dir = cache_dir
        self.prompt_file = os.path.join(cache_dir, "gemini_upload.jsonl")
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

    def compile_jsonl(self) -> int:
        """
        Compile all cached pages into a single JSONL file for Gemini file store upload.
        Each line is a JSON object with url, title, scrape_date, tags, and content.
        Returns the number of records written.
        """
        out_path = os.path.join(self.cache_dir, "gemini_upload.jsonl")
        records_written = 0

        with open(out_path, "w", encoding="utf-8") as out_file:
            for filename in sorted(os.listdir(self.cache_dir)):
                if not filename.endswith(".txt"):
                    continue

                filepath = os.path.join(self.cache_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        raw = f.read()

                    # Parse header written by _save_to_cache
                    lines = raw.splitlines()
                    url = ""
                    scrape_date = ""
                    content_start = 0
                    for i, line in enumerate(lines):
                        if line.startswith("URL: "):
                            url = line[5:].strip()
                        elif line.startswith("Extraction Time: "):
                            scrape_date = line[17:].strip()
                        elif line.startswith("-" * 20):
                            content_start = i + 1
                            break

                    content_lines = lines[content_start:]
                    content = _clean_unicode("\n".join(content_lines).strip())

                    # Use first non-empty content line as title
                    title = next((l for l in content_lines if l.strip()), url)
                    title = _clean_unicode(title.strip())[:200]  # cap length

                    # Derive tags from domain
                    domain = urlparse(url).netloc if url else ""
                    tags = [domain] if domain else []

                    record = {
                        "url": url,
                        "title": title,
                        "scrape_date": scrape_date,
                        "tags": tags,
                        "content": content,
                    }
                    out_file.write(json.dumps(record, ensure_ascii=False) + "\n")
                    records_written += 1

                except Exception as e:
                    logger.warning(f"Skipping {filename}: {e}")

        logger.info(f"Compiled {records_written} records to {out_path}")
        return records_written

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

    def log_current_gemini_state(self, stage="CURRENT"):
        """
        Logs all existing file search stores and the files within them.
        """
        if not self.gemini_client:
            logger.info(f"--- Gemini client not initialized. Cannot log {stage} state. ---")
            return

        logger.info(f"--- Gemini Knowledge State: {stage} ---")
        try:
            stores = list(self.gemini_client.file_search_stores.list())
            if not stores:
                logger.info("No file search stores found.")
                return

            for store in stores:
                logger.info(f"Store: {store.display_name} | Name: {store.name} | Size: {store.size_bytes} bytes | Created: {store.create_time}")
                try:
                    # Attempt to list files in the store
                    files = list(self.gemini_client.file_search_stores.files.list(file_search_store_name=store.name))
                    if files:
                        for f in files:
                            logger.info(f"  -> File: {f.display_name} | Name: {f.name} | Size: {f.size_bytes if hasattr(f, 'size_bytes') else 'N/A'}")
                    else:
                        logger.info("  -> (No files found in this store)")
                except Exception as file_e:
                    logger.debug(f"Could not list files for store {store.name}: {file_e}")
        except Exception as e:
            logger.error(f"Error logging Gemini state: {e}")
        logger.info("-" * 40)

    def update_gemini_store(self):
        """
        Uploads the compiled prompt file to Gemini's file search store.
        """
        if not self.gemini_client:
            logger.error("Gemini client not initialized. Cannot update file store.")
            return

        store_name = 'emanuel_scrape_store'
        
        try:
            # log state before
            self.log_current_gemini_state("BEFORE Update")

            logger.info(f"Checking for Gemini file search store: {store_name}")
            
            # Delete all existing stores with this name before creating a fresh one
            existing = [s for s in self.gemini_client.file_search_stores.list() if s.display_name == store_name]
            if existing:
                logger.info(f"Deleting {len(existing)} existing store(s) named '{store_name}'...")
                for store in existing:
                    self.gemini_client.file_search_stores.delete(name=store.name, config={"force": True})
                    logger.info(f"  Deleted {store.name}")

            logger.info(f"Creating new file search store: {store_name}")
            file_search_store = self.gemini_client.file_search_stores.create(config={'display_name': store_name})

            logger.info(f"Uploading {self.prompt_file} to Gemini...")

            operation = self.gemini_client.file_search_stores.upload_to_file_search_store(
                file=self.prompt_file,
                file_search_store_name=file_search_store.name,
                config={'display_name': 'emanuel_prompt', 'mime_type': 'text/plain'}
            )

            # Gemini indexes the file asynchronously — done=None until indexing completes
            # which can take several minutes. We don't block here; the store will be ready
            # once Gemini finishes processing in the background.
            logger.info(f"Upload submitted. Gemini is indexing asynchronously.")
            logger.info(f"Operation: {operation.name}")

            # log state after
            self.log_current_gemini_state("AFTER Update")
            
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

    def run(self, skip_scrape: bool = False, compile_only: bool = False) -> dict:
        """
        Main entry point - run the scraping and compilation workflow.

        Args:
            skip_scrape:   Skip scraping; recompile JSONL from cache and upload.
            compile_only:  Skip scraping and upload; only recompile JSONL from cache.

        Returns a summary of the operation.
        """
        start_time = time.time()
        summary = {"sites_scraped": [], "total_pages": 0, "total_chars_saved": 0}

        if compile_only:
            logger.info("Compile-only mode — regenerating JSONL from cache, no upload.")
            summary["records_compiled"] = self.compile_jsonl()
        elif skip_scrape:
            logger.info(f"Skipping scrape — recompiling JSONL and uploading {self.prompt_file}")
            summary["records_compiled"] = self.compile_jsonl()
            self.update_gemini_store()
        else:
            self.log_current_gemini_state("BEFORE SCRAPE")
            sites = [
                "https://www.loopnlearn.org/",
                "https://loopkit.github.io/loopdocs/",
            ]
            summary = asyncio.run(self._run_async(sites))
            summary["records_compiled"] = self.compile_jsonl()
            self.update_gemini_store()

        end_time = time.time()
        summary["time_taken_seconds"] = round(end_time - start_time, 2)

        logger.info(
            f"Done: {summary['total_pages']} pages scraped, "
            f"{summary['total_chars_saved']:,} chars in {summary['time_taken_seconds']}s"
        )

        return summary


# Convenience function for sync contexts
def run_scraper(cache_dir: str = "backend/cache", skip_scrape: bool = False, compile_only: bool = False) -> dict:
    """Run the scraper with specified configuration."""
    scraper = ScraperService(cache_dir=cache_dir)
    return scraper.run(skip_scrape=skip_scrape, compile_only=compile_only)


if __name__ == "__main__":
    '''
    # Bara regenerera JSONL-filen (se om unicode-städningen fungerar)
    python3 backend/app/services/scraper.py --compile-only

    # Recompile + ladda upp utan att scrapa
    python3 backend/app/services/scraper.py --skip-scrape

    # Fullt flöde
    python3 backend/app/services/scraper.py
    
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping; recompile JSONL from cache and upload")
    parser.add_argument("--compile-only", action="store_true", help="Only recompile JSONL from cache, no upload")
    args = parser.parse_args()

    cwd = os.getcwd()
    cache_dir = "cache" if cwd.endswith("backend") else "backend/cache"

    result = run_scraper(cache_dir=cache_dir, skip_scrape=args.skip_scrape, compile_only=args.compile_only)
    print(f"\n{'='*50}")
    print("Scraping Summary:")
    print(f"  Sites: {len(result['sites_scraped'])}")
    print(f"  Pages: {result['total_pages']}")
    print(f"  Characters: {result['total_chars_saved']:,}")
    print(f"  Time: {result['time_taken_seconds']}s")
    print(f"{'='*50}")
