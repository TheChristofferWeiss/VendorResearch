"""
Web scraper using trafilatura and markdownify for clean content extraction.
"""

import requests
import trafilatura
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import time
import logging
from urllib.parse import urljoin, urlparse
import os

logger = logging.getLogger(__name__)

class WebScraper:
    """Web scraper that extracts clean content using trafilatura and converts to markdown."""
    
    def __init__(self, user_agent: str = None, delay: float = 1.0):
        self.user_agent = user_agent or os.getenv('USER_AGENT', 'VendorResearchBot/1.0')
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_url(self, url: str) -> Optional[Dict]:
        """
        Scrape a single URL and extract clean content.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary with extracted content, metadata, and markdown
        """
        try:
            logger.info(f"Scraping URL: {url}")
            
            # Add delay between requests
            if self.delay > 0:
                time.sleep(self.delay)
            
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            html_content = response.text
            
            # Extract content using trafilatura
            extracted_content = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=True,
                include_images=False,
                include_links=True
            )
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(html_content)
            
            # Convert to markdown if content was extracted
            markdown_content = None
            if extracted_content:
                # Use markdownify to convert HTML to markdown
                markdown_content = md(extracted_content, heading_style="ATX")
            
            # Extract links for potential further crawling
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if self._is_valid_link(full_url, url):
                    links.append({
                        'url': full_url,
                        'text': link.get_text(strip=True),
                        'title': link.get('title', '')
                    })
            
            result = {
                'url': url,
                'title': metadata.title if metadata else None,
                'author': metadata.author if metadata else None,
                'date': metadata.date if metadata else None,
                'description': metadata.description if metadata else None,
                'content': extracted_content,
                'markdown': markdown_content,
                'links': links,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'scraped_at': time.time()
            }
            
            logger.info(f"Successfully scraped {url}")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def _is_valid_link(self, link_url: str, base_url: str) -> bool:
        """Check if a link is valid for crawling."""
        try:
            parsed_link = urlparse(link_url)
            parsed_base = urlparse(base_url)
            
            # Skip external links
            if parsed_link.netloc != parsed_base.netloc:
                return False
            
            # Skip common non-content URLs
            skip_patterns = [
                '/login', '/signup', '/register', '/logout',
                '/search', '/cart', '/checkout', '/account',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx',
                '.zip', '.rar', '.tar', '.gz',
                'javascript:', 'mailto:', 'tel:'
            ]
            
            for pattern in skip_patterns:
                if pattern in link_url.lower():
                    return False
            
            return True
            
        except Exception:
            return False
    
    def scrape_multiple_urls(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraped content dictionaries
        """
        results = []
        for url in urls:
            result = self.scrape_url(url)
            if result:
                results.append(result)
        return results
