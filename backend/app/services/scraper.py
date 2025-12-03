import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScraperService:
    def __init__(self, cache_dir: str = "backend/cache", prompt_file: str = "backend/emanuel_prompt.txt"):
        self.cache_dir = cache_dir
        self.prompt_file = prompt_file
        self.visited_urls = set()
        
        # Ensure cache directory exists
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def is_valid_url(self, url: str, base_domain: str) -> bool:
        """
        Checks if the URL is valid and belongs to the base domain.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme) and base_domain in parsed.netloc

    def get_all_website_links(self, url: str) -> set:
        """
        Returns all URLs that are found on `url` and belongs to the same website.
        """
        urls = set()
        domain_name = urlparse(url).netloc
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Error crawling {url}: {e}")
            return urls

        soup = BeautifulSoup(response.content, "html.parser")
        
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            
            # Join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            
            parsed_href = urlparse(href)
            
            # Remove URL fragment identifiers
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            
            if not self.is_valid_url(href, domain_name):
                continue
            
            # Ignore PDF files
            if href.lower().endswith(".pdf"):
                continue
            
            if href in self.visited_urls:
                continue
                
            urls.add(href)
            
        return urls

    def scrape_site(self, start_url: str) -> dict:
        """
        Crawls the site starting from `start_url` and extracts text.
        Returns stats for the site.
        """
        logger.info(f"Starting scrape for {start_url}")
        urls_to_visit = {start_url}
        domain_name = urlparse(start_url).netloc
        
        site_stats = {
            "url": start_url,
            "pages_scraped": 0,
            "chars_saved": 0
        }
        
        while urls_to_visit:
            current_url = urls_to_visit.pop()
            if current_url in self.visited_urls:
                continue
            
            # Double check for PDF before scraping (in case it was added before filter)
            if current_url.lower().endswith(".pdf"):
                continue

            logger.info(f"Scraping: {current_url}")
            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                
                chars = self.save_to_cache(current_url, response.text)
                self.visited_urls.add(current_url)
                site_stats["pages_scraped"] += 1
                site_stats["chars_saved"] += chars
                
                # Find more links
                new_links = self.get_all_website_links(current_url)
                urls_to_visit.update(new_links)
                
                # Be polite
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to scrape {current_url}: {e}")
        
        return site_stats

    def save_to_cache(self, url: str, html_content: str) -> int:
        """
        Extracts text from HTML and saves it to a file in the cache directory.
        Returns the number of characters saved.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Specific logic for loopandlearn.org
        if "loopnlearn.org" in url:
            # Target main content area
            main_area = soup.find(id="et-main-area")
            if main_area:
                soup = main_area
            
            # Remove footer
            footer = soup.find(id="main-footer")
            if footer:
                footer.extract()

        # Specific logic for loopkit.github.io
        if "loopkit.github.io" in url:
            # Target main content area
            main_area = soup.find(class_="md-content")
            if main_area:
                soup = main_area
            
        text = soup.get_text(separator='\n')
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Create a safe filename
        safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + ".txt"
        filepath = os.path.join(self.cache_dir, safe_filename)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"URL: {url}\nExtraction Time: {timestamp}\n{'-' * 20}\n{text}"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return len(content)

    def compile_prompt(self):
        """
        Reads all cached files and creates the prompt file.
        Also saves the prompt to Firestore.
        """
        logger.info("Compiling prompt file...")
        full_prompt = ""
        
        # Header
        full_prompt += "You are Emanuel, an AI assistant for the Nightscout and Loop community.\n"
        full_prompt += "Explicitly only answer using the information in the following context.\n"
        full_prompt += "Always answer with clickable links and clear instructions.\n"
        full_prompt += "If the answer is not in the context, state that you don't know based on the available information.\n\n"
        full_prompt += "=== CONTEXT START ===\n\n"
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.cache_dir, filename)
                with open(filepath, "r", encoding="utf-8") as infile:
                    full_prompt += infile.read()
                    full_prompt += "\n\n" + "=" * 40 + "\n\n"
        
        full_prompt += "=== CONTEXT END ===\n"
        
        # Save to file
        with open(self.prompt_file, "w", encoding="utf-8") as outfile:
            outfile.write(full_prompt)
        logger.info(f"Prompt file created at {self.prompt_file}")
        
        # Save to Firestore
        try:
            # Try to import here to avoid circular imports or issues when running as script without proper path
            # Note: This assumes the script is run in a way that 'app' module is resolvable 
            # or we are in the backend context.
            from ..services.firebase import save_emanuel_prompt
            save_emanuel_prompt(full_prompt)
        except ImportError:
            logger.warning("Could not import save_emanuel_prompt from app.services.firebase. Skipping Firestore save.")
        except Exception as e:
            logger.error(f"Failed to save to Firestore: {e}")

    def run(self) -> dict:
        """
        Main entry point to run the scraping and compilation.
        Returns a summary of the operation.

        # maybee add later: "https://github.com/nightscout/cgm-remote-monitor" 
        """
        start_time = time.time()
        
        sites = [
            "https://www.loopnlearn.org/",
            "https://loopkit.github.io/loopdocs/",            
        ]
        
        summary = {
            "sites_scraped": [],
            "total_pages": 0,
            "total_chars_saved": 0,
            "time_taken_seconds": 0
        }
        
        for site in sites:
            site_stats = self.scrape_site(site)
            summary["sites_scraped"].append(site_stats)
            summary["total_pages"] += site_stats["pages_scraped"]
            summary["total_chars_saved"] += site_stats["chars_saved"]
            
        self.compile_prompt()
        
        end_time = time.time()
        summary["time_taken_seconds"] = round(end_time - start_time, 2)
        
        return summary

if __name__ == "__main__":
    # Adjust paths for running as a script from the root or backend dir
    # Assuming running from project root: python backend/app/services/scraper.py
    # But the code defaults to "backend/cache", so we need to be careful about CWD.
    
    # If running directly, let's try to detect if we are in backend or root
    cwd = os.getcwd()
    if cwd.endswith("backend"):
        cache_dir = "cache"
        prompt_file = "emanuel_prompt.txt"
    else:
        cache_dir = "backend/cache"
        prompt_file = "backend/emanuel_prompt.txt"
        
    scraper = ScraperService(cache_dir=cache_dir, prompt_file=prompt_file)
    scraper.run()
