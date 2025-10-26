"""
Scraper service for the Vendor Research Web Application.
"""

import requests
import subprocess
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class ScraperService:
    """Service for scraping vendor websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_vendor(self, url):
        """Scrape a vendor website and return structured data."""
        try:
            print(f"Starting scrape of: {url}")
            
            # Use curl to fetch the content (bypassing SSL issues)
            content = self._fetch_url_with_curl(url)
            if not content:
                return None
            
            # Parse with Beautiful Soup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract basic information
            vendor_info = self._extract_basic_info(soup, url)
            
            # Find all relevant pages
            relevant_pages = self._find_relevant_pages(soup, url)
            
            print(f"Found {len(relevant_pages)} relevant pages to scrape")
            
            # Scrape each relevant page
            all_content = []
            for page_url in relevant_pages:
                print(f"Scraping page: {page_url}")
                page_content = self._fetch_url_with_curl(page_url)
                if page_content:
                    page_soup = BeautifulSoup(page_content, 'html.parser')
                    page_data = self._extract_page_content(page_soup, page_url)
                    all_content.append(page_data)
                time.sleep(1)  # Be respectful
            
            # Combine all content
            vendor_info['pages'] = all_content
            vendor_info['total_pages_scraped'] = len(all_content)
            
            return vendor_info
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def _fetch_url_with_curl(self, url):
        """Fetch URL content using curl."""
        try:
            cmd = [
                'curl', '-s', '-L', '--max-time', '30',
                '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Curl error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _extract_basic_info(self, soup, url):
        """Extract basic vendor information."""
        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Extract vendor name
        vendor_name = self._extract_vendor_name(title_text, url)
        
        # Extract contact info from main page
        main_content = soup.get_text()
        contact_info = self._extract_contact_info(main_content)
        
        return {
            'url': url,
            'name': vendor_name,
            'title': title_text,
            'description': description,
            'contact_info': contact_info,
            'scraped_at': time.time()
        }
    
    def _find_relevant_pages(self, soup, base_url):
        """Find all relevant pages (products, services, etc.) excluding blogs."""
        relevant_pages = [base_url]  # Include main page
        
        # Find all links first
        links = soup.find_all('a', href=True)
        print(f"Total links found: {len(links)}")
        
        # Collect all unique URLs
        all_urls = set()
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            all_urls.add(full_url)
        
        print(f"Unique URLs found: {len(all_urls)}")
        
        # Filter for relevant pages
        for url in all_urls:
            if self._is_relevant_page(url, base_url):
                if url not in relevant_pages:
                    relevant_pages.append(url)
        
        return relevant_pages
    
    def _is_relevant_page(self, url, base_url):
        """Check if a page is relevant (not blog, not external, etc.)."""
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            
            # Must be same domain
            if parsed_url.netloc != parsed_base.netloc:
                return False
            
            # Skip common non-content URLs
            skip_patterns = [
                '/login', '/signup', '/register', '/logout',
                '/search', '/cart', '/checkout', '/account',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx',
                '.zip', '.rar', '.tar', '.gz',
                'javascript:', 'mailto:', 'tel:',
                '#',  # Skip anchors
                '/wp-admin', '/admin', '/dashboard'
            ]
            
            for pattern in skip_patterns:
                if pattern in url.lower():
                    return False
            
            # Skip query parameters for now (but include main pages)
            if '?' in url and url != base_url:
                return False
            
            # Include main domain and subpages
            return True
            
        except Exception:
            return False
    
    def _extract_page_content(self, soup, url):
        """Extract content from a specific page."""
        # Get page title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Extract main content
        main_content = self._extract_main_content(soup)
        
        # Extract contact info from this page
        contact_info = self._extract_contact_info(main_content)
        
        # Extract services/products mentioned
        services = self._extract_services(main_content)
        
        # Extract technology stack
        tech_stack = self._extract_technology_stack(main_content)
        
        return {
            'url': url,
            'title': title_text,
            'content': main_content,
            'contact_info': contact_info,
            'services': services,
            'technology_stack': tech_stack
        }
    
    def _extract_main_content(self, soup):
        """Extract main content from page."""
        # Try to find main content areas
        content_selectors = [
            'main', 'article', '.content', '#content', '.main-content',
            '.page-content', '.post-content', '.entry-content',
            '.services', '.products', '.solutions'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback to body
        body = soup.find('body')
        if body:
            return body.get_text(strip=True)
        
        return ""
    
    def _extract_contact_info(self, content):
        """Extract contact information from content."""
        contact_info = {}
        
        # Extract emails
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = email_pattern.findall(content)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone numbers
        phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
        phones = phone_pattern.findall(content)
        if phones:
            contact_info['phone'] = ''.join(phones[0])
        
        return contact_info
    
    def _extract_services(self, content):
        """Extract services mentioned in content."""
        service_keywords = [
            'consulting', 'development', 'design', 'marketing', 'analytics',
            'cloud', 'hosting', 'support', 'maintenance', 'integration',
            'custom software', 'web development', 'mobile app', 'e-commerce',
            'data analytics', 'business intelligence', 'automation', 'AI',
            'machine learning', 'cybersecurity', 'devops', 'infrastructure',
            'training', 'implementation', 'migration', 'optimization'
        ]
        
        services = []
        content_lower = content.lower()
        
        for keyword in service_keywords:
            if keyword in content_lower:
                services.append(keyword.title())
        
        return list(set(services))
    
    def _extract_technology_stack(self, content):
        """Extract technology stack mentioned in content."""
        tech_keywords = [
            'python', 'javascript', 'react', 'vue', 'angular', 'node.js',
            'java', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'apache', 'nginx', 'linux', 'windows', 'macos'
        ]
        
        tech_stack = []
        content_lower = content.lower()
        
        for tech in tech_keywords:
            if tech in content_lower:
                tech_stack.append(tech.title())
        
        return list(set(tech_stack))
    
    def _extract_vendor_name(self, title, url):
        """Extract vendor name from title or URL."""
        if title:
            # Remove common suffixes
            title = re.sub(r'\s*-\s*(Home|About|Services|Contact).*$', '', title, flags=re.IGNORECASE)
            return title.strip()
        
        # Fallback to domain name
        domain = urlparse(url).netloc.replace('www.', '')
        return domain.replace('.fi', '').replace('.com', '').title()
