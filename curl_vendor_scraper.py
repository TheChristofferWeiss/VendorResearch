"""
Curl-based Vendor Scraper - Uses curl to bypass Python SSL issues
"""

import json
import re
import time
import subprocess
import os
from urllib.parse import urljoin, urlparse
from datetime import datetime
from bs4 import BeautifulSoup

class CurlVendorScraper:
    """Vendor scraper that uses curl to fetch content."""
    
    def __init__(self):
        # Regex patterns for extraction
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
    
    def fetch_url_with_curl(self, url):
        """Fetch URL content using curl."""
        try:
            print(f"Fetching: {url}")
            
            # Use curl to fetch the content
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
    
    def scrape_vendor_site(self, base_url):
        """Scrape entire vendor website, focusing on products/services."""
        print(f"Starting comprehensive scrape of: {base_url}")
        
        # Fetch main page
        main_content = self.fetch_url_with_curl(base_url)
        if not main_content:
            print("Failed to fetch main page")
            return None
        
        # Parse main page
        soup = BeautifulSoup(main_content, 'html.parser')
        
        # Extract basic info from main page
        vendor_info = self._extract_basic_info(soup, base_url)
        
        # Find all relevant pages (products, services, etc.)
        relevant_pages = self._find_relevant_pages(soup, base_url)
        
        print(f"Found {len(relevant_pages)} relevant pages to scrape")
        
        # Scrape each relevant page
        all_content = []
        for page_url in relevant_pages:
            print(f"Scraping page: {page_url}")
            page_content = self.fetch_url_with_curl(page_url)
            if page_content:
                page_soup = BeautifulSoup(page_content, 'html.parser')
                page_data = self._extract_page_content(page_soup, page_url)
                all_content.append(page_data)
            time.sleep(1)  # Be respectful
        
        # Combine all content
        vendor_info['pages'] = all_content
        vendor_info['total_pages_scraped'] = len(all_content)
        
        return vendor_info
    
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
            'scraped_at': datetime.now().isoformat()
        }
    
    def _find_relevant_pages(self, soup, base_url):
        """Find all relevant pages (products, services, etc.) excluding blogs."""
        relevant_pages = [base_url]  # Include main page
        
        # Keywords for relevant pages
        relevant_keywords = [
            'services', 'products', 'solutions', 'offerings', 'portfolio',
            'about', 'company', 'team', 'contact', 'pricing', 'plans',
            'features', 'capabilities', 'expertise', 'industries'
        ]
        
        # Keywords to exclude (blogs, news, etc.)
        exclude_keywords = [
            'blog', 'news', 'article', 'post', 'journal', 'diary',
            'updates', 'announcements', 'press', 'media'
        ]
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # Check if it's a valid internal link
            if self._is_valid_internal_link(full_url, base_url):
                link_text = link.get_text().lower().strip()
                url_path = urlparse(full_url).path.lower()
                
                # Check if it contains relevant keywords
                is_relevant = any(keyword in link_text or keyword in url_path 
                                for keyword in relevant_keywords)
                
                # Check if it should be excluded
                is_excluded = any(keyword in link_text or keyword in url_path 
                                for keyword in exclude_keywords)
                
                if is_relevant and not is_excluded:
                    if full_url not in relevant_pages:
                        relevant_pages.append(full_url)
        
        return relevant_pages
    
    def _is_valid_internal_link(self, link_url, base_url):
        """Check if link is a valid internal link."""
        try:
            parsed_link = urlparse(link_url)
            parsed_base = urlparse(base_url)
            
            # Must be same domain
            if parsed_link.netloc != parsed_base.netloc:
                return False
            
            # Skip common non-content URLs
            skip_patterns = [
                '/login', '/signup', '/register', '/logout',
                '/search', '/cart', '/checkout', '/account',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx',
                '.zip', '.rar', '.tar', '.gz',
                'javascript:', 'mailto:', 'tel:',
                '#', '?'  # Skip anchors and query params for now
            ]
            
            for pattern in skip_patterns:
                if pattern in link_url.lower():
                    return False
            
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
        emails = self.email_pattern.findall(content)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone numbers
        phones = self.phone_pattern.findall(content)
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
    
    def save_results(self, vendor_info, output_dir="research_output"):
        """Save comprehensive results to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        vendor_name = vendor_info['name'].replace(' ', '_').replace('/', '_')
        vendor_dir = os.path.join(output_dir, vendor_name)
        os.makedirs(vendor_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save comprehensive vendor info
        with open(os.path.join(vendor_dir, 'comprehensive_vendor_info.json'), 'w', encoding='utf-8') as f:
            json.dump(vendor_info, f, indent=2, ensure_ascii=False)
        
        # Create comprehensive markdown report
        report = self._generate_comprehensive_report(vendor_info)
        with open(os.path.join(vendor_dir, 'comprehensive_report.md'), 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save individual page content
        for i, page in enumerate(vendor_info.get('pages', []), 1):
            page_filename = f"page_{i}_{urlparse(page['url']).path.replace('/', '_').strip('_')}.md"
            if not page_filename.endswith('.md'):
                page_filename += '.md'
            
            page_content = f"""# {page['title']}

**URL**: {page['url']}

## Content

{page['content']}

## Services Mentioned
{', '.join(page['services']) if page['services'] else 'None found'}

## Technology Stack
{', '.join(page['technology_stack']) if page['technology_stack'] else 'None found'}

## Contact Information
{json.dumps(page['contact_info'], indent=2) if page['contact_info'] else 'None found'}
"""
            
            with open(os.path.join(vendor_dir, page_filename), 'w', encoding='utf-8') as f:
                f.write(page_content)
        
        print(f"\nComprehensive results saved to: {vendor_dir}")
        return vendor_dir
    
    def _generate_comprehensive_report(self, vendor_info):
        """Generate comprehensive markdown report."""
        report = f"""# Comprehensive Vendor Research Report: {vendor_info['name']}

## Basic Information
- **Website**: {vendor_info['url']}
- **Title**: {vendor_info['title']}
- **Description**: {vendor_info['description']}
- **Total Pages Scraped**: {vendor_info.get('total_pages_scraped', 0)}

## Contact Information
"""
        
        for key, value in vendor_info['contact_info'].items():
            report += f"- **{key.title()}**: {value}\n"
        
        # Aggregate services from all pages
        all_services = set()
        all_tech_stack = set()
        
        for page in vendor_info.get('pages', []):
            all_services.update(page.get('services', []))
            all_tech_stack.update(page.get('technology_stack', []))
        
        if all_services:
            report += "\n## All Services Found\n"
            for service in sorted(all_services):
                report += f"- {service}\n"
        
        if all_tech_stack:
            report += "\n## Technology Stack\n"
            for tech in sorted(all_tech_stack):
                report += f"- {tech}\n"
        
        report += "\n## Pages Scraped\n"
        for i, page in enumerate(vendor_info.get('pages', []), 1):
            report += f"\n### {i}. {page['title']}\n"
            report += f"- **URL**: {page['url']}\n"
            report += f"- **Services**: {', '.join(page.get('services', []))}\n"
            report += f"- **Content Preview**: {page['content'][:200]}...\n"
        
        report += f"\n---\n*Report generated on: {vendor_info['scraped_at']}*"
        
        return report

def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python curl_vendor_scraper.py <vendor_url>")
        print("Example: python curl_vendor_scraper.py https://www.ammattipuhuja.fi")
        return
    
    url = sys.argv[1]
    
    scraper = CurlVendorScraper()
    vendor_info = scraper.scrape_vendor_site(url)
    
    if vendor_info:
        print(f"\n✓ Successfully scraped {vendor_info['name']}")
        print(f"  Total pages: {vendor_info.get('total_pages_scraped', 0)}")
        
        # Save results
        output_dir = scraper.save_results(vendor_info)
        
        print(f"\nComprehensive vendor research completed!")
        print(f"Results saved to: {output_dir}")
    else:
        print("Failed to scrape vendor information.")

if __name__ == "__main__":
    main()
