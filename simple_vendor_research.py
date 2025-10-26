"""
Simple Vendor Research Tool - Uses only built-in Python libraries and requests/beautifulsoup4
"""

import requests
import json
import re
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import os

class SimpleVendorResearcher:
    """Simple vendor research tool using only available libraries."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'VendorResearchBot/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Regex patterns for extraction
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
        self.price_pattern = re.compile(r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day))?', re.IGNORECASE)
    
    def scrape_vendor(self, url):
        """Scrape a vendor website and extract information."""
        try:
            print(f"Scraping: {url}")
            
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse with Beautiful Soup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic information
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Extract main content (try to find main content areas)
            content_selectors = [
                'main', 'article', '.content', '#content', '.main-content',
                '.page-content', '.post-content', '.entry-content'
            ]
            
            main_content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    main_content = element.get_text(strip=True)
                    break
            
            # Fallback to body if no main content found
            if not main_content:
                body = soup.find('body')
                if body:
                    main_content = body.get_text(strip=True)
            
            # Extract metadata
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            
            # Extract contact information
            contact_info = self._extract_contact_info(main_content)
            
            # Extract services
            services = self._extract_services(main_content)
            
            # Extract technology stack
            tech_stack = self._extract_technology_stack(main_content)
            
            # Extract links
            links = self._extract_links(soup, url)
            
            # Extract vendor name
            vendor_name = self._extract_vendor_name(title_text, url)
            
            return {
                'url': url,
                'name': vendor_name,
                'title': title_text,
                'description': description,
                'content': main_content[:1000] + '...' if len(main_content) > 1000 else main_content,
                'contact_info': contact_info,
                'services': services,
                'technology_stack': tech_stack,
                'links': links[:10],  # Limit to first 10 links
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def _extract_contact_info(self, content):
        """Extract contact information from content."""
        contact_info = {}
        
        # Extract emails
        emails = self.email_pattern.findall(content)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone numbers
        phones = self.phone_pattern.findall(content)
        if phones:
            contact_info['phone'] = ''.join(phones[0])
        
        return contact_info
    
    def _extract_services(self, content):
        """Extract services offered by the vendor."""
        service_keywords = [
            'consulting', 'development', 'design', 'marketing', 'analytics',
            'cloud', 'hosting', 'support', 'maintenance', 'integration',
            'custom software', 'web development', 'mobile app', 'e-commerce',
            'data analytics', 'business intelligence', 'automation', 'AI',
            'machine learning', 'cybersecurity', 'devops', 'infrastructure'
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
    
    def _extract_links(self, soup, base_url):
        """Extract relevant links from the page."""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            text = link.get_text(strip=True)
            
            if self._is_valid_link(full_url, base_url) and text:
                links.append({
                    'url': full_url,
                    'text': text
                })
        
        return links
    
    def _is_valid_link(self, link_url, base_url):
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
    
    def _extract_vendor_name(self, title, url):
        """Extract vendor name from title or URL."""
        if title:
            # Remove common suffixes
            title = re.sub(r'\s*-\s*(Home|About|Services|Contact).*$', '', title, flags=re.IGNORECASE)
            return title.strip()
        
        # Fallback to domain name
        domain = urlparse(url).netloc
        return domain.replace('www.', '')
    
    def research_vendors(self, urls):
        """Research multiple vendors."""
        results = []
        
        print(f"Starting research for {len(urls)} vendor(s)...")
        print("=" * 50)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing: {url}")
            result = self.scrape_vendor(url)
            
            if result:
                results.append(result)
                print(f"✓ Successfully scraped: {result['name']}")
                print(f"  Services: {', '.join(result['services'][:3]) if result['services'] else 'None found'}")
                print(f"  Contact: {result['contact_info'].get('email', 'None found')}")
            else:
                print(f"✗ Failed to scrape: {url}")
            
            # Add delay between requests
            time.sleep(1)
        
        return results
    
    def save_results(self, results, output_dir="research_output"):
        """Save results to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual results
        for result in results:
            vendor_name = result['name'].replace(' ', '_').replace('/', '_')
            vendor_dir = os.path.join(output_dir, vendor_name)
            os.makedirs(vendor_dir, exist_ok=True)
            
            # Save vendor info
            with open(os.path.join(vendor_dir, 'vendor_info.json'), 'w') as f:
                json.dump(result, f, indent=2)
        
        # Save summary
        summary_file = os.path.join(output_dir, f"summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {output_dir}")
        print(f"Summary saved to: {summary_file}")
        
        return summary_file
    
    def display_results(self, results):
        """Display results in a simple format."""
        if not results:
            print("No results to display.")
            return
        
        print("\n" + "=" * 60)
        print("VENDOR RESEARCH RESULTS")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['name']}")
            print(f"   URL: {result['url']}")
            print(f"   Description: {result['description'][:100]}..." if result['description'] else "   Description: None")
            
            if result['contact_info']:
                print("   Contact:")
                for key, value in result['contact_info'].items():
                    print(f"     {key.title()}: {value}")
            
            if result['services']:
                print(f"   Services: {', '.join(result['services'][:5])}")
            
            if result['technology_stack']:
                print(f"   Tech Stack: {', '.join(result['technology_stack'][:5])}")

def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_vendor_research.py <url1> [url2] [url3] ...")
        print("Example: python simple_vendor_research.py https://example.com https://another-vendor.com")
        return
    
    urls = sys.argv[1:]
    
    researcher = SimpleVendorResearcher()
    results = researcher.research_vendors(urls)
    
    if results:
        researcher.display_results(results)
        researcher.save_results(results)
    else:
        print("No results obtained.")

if __name__ == "__main__":
    main()
