"""
Simple Web Server for Vendor Research
A minimal web interface that works with available packages.
"""

import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
import subprocess
import threading
import time
import re
import socket
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class SimpleVendorDB:
    """Simple SQLite database for vendors."""
    
    def __init__(self, db_path='vendor_research.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                website TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                raw_data TEXT,
                scraped_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                url TEXT,
                pricing TEXT,
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                url TEXT,
                pricing TEXT,
                target_audience TEXT,
                requirements TEXT,
                deployment TEXT,
                support TEXT,
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id INTEGER,
                feature TEXT NOT NULL,
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                feature TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_vendor(self, name, website, description=''):
        """Add a new vendor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO vendors (name, website, description) VALUES (?, ?, ?)',
            (name, website, description)
        )
        vendor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vendor_id
    
    def remove_vendor(self, vendor_id):
        """Remove a vendor and all associated data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Remove service features first
        cursor.execute('DELETE FROM service_features WHERE service_id IN (SELECT id FROM services WHERE vendor_id = ?)', (vendor_id,))
        
        # Remove product features
        cursor.execute('DELETE FROM product_features WHERE product_id IN (SELECT id FROM products WHERE vendor_id = ?)', (vendor_id,))
        
        # Remove services
        cursor.execute('DELETE FROM services WHERE vendor_id = ?', (vendor_id,))
        
        # Remove products
        cursor.execute('DELETE FROM products WHERE vendor_id = ?', (vendor_id,))
        
        # Remove vendor
        cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def get_vendors(self):
        """Get all vendors."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors ORDER BY created_at DESC')
        vendors = cursor.fetchall()
        conn.close()
        return vendors
    
    def get_vendor(self, vendor_id):
        """Get a specific vendor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,))
        vendor = cursor.fetchone()
        conn.close()
        return vendor
    
    def update_vendor_status(self, vendor_id, status, raw_data=None):
        """Update vendor status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE vendors SET status = ?, raw_data = ?, scraped_at = ? WHERE id = ?',
            (status, raw_data, datetime.now().isoformat(), vendor_id)
        )
        conn.commit()
        conn.close()
    
    def get_vendor_services(self, vendor_id):
        """Get services for a vendor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services WHERE vendor_id = ?', (vendor_id,))
        services = cursor.fetchall()
        conn.close()
        return services
    
    def get_vendor_products(self, vendor_id):
        """Get products for a vendor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE vendor_id = ?', (vendor_id,))
        products = cursor.fetchall()
        conn.close()
        return products
    
    def add_service(self, vendor_id, name, category, description, url, pricing):
        """Add a service."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO services (vendor_id, name, category, description, url, pricing) VALUES (?, ?, ?, ?, ?, ?)',
            (vendor_id, name, category, description, url, pricing)
        )
        service_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return service_id
    
    def add_product(self, vendor_id, name, category, description, url, pricing, target_audience, requirements, deployment, support):
        """Add a product."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (vendor_id, name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (vendor_id, name, category, description, url, pricing, target_audience, requirements, deployment, support)
        )
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id

class SimpleScraper:
    """Simple web scraper."""
    
    def __init__(self):
        self.progress_callbacks = {}
    
    def set_progress_callback(self, vendor_id, callback):
        """Set progress callback for a vendor."""
        self.progress_callbacks[vendor_id] = callback
    
    def scrape_vendor(self, vendor_id, url):
        """Scrape a vendor website."""
        try:
            print(f"[{vendor_id}] Starting scrape of: {url}")
            self._update_progress(vendor_id, 0, "Starting scrape...")
            
            content = self._fetch_url_with_curl(url)
            if not content:
                self._update_progress(vendor_id, 100, "Failed to fetch main page")
                return None
            
            self._update_progress(vendor_id, 20, "Main page fetched, parsing...")
            
            soup = BeautifulSoup(content, 'html.parser')
            
            vendor_info = self._extract_basic_info(soup, url)
            
            self._update_progress(vendor_id, 40, "Basic info extracted, finding pages...")
            
            relevant_pages = self._find_relevant_pages(soup, url)
            
            print(f"[{vendor_id}] Found {len(relevant_pages)} relevant pages to scrape")
            self._update_progress(vendor_id, 50, f"Found {len(relevant_pages)} pages to scrape")
            
            all_content = []
            total_pages = len(relevant_pages[:5])
            
            for i, page_url in enumerate(relevant_pages[:5]):
                print(f"[{vendor_id}] Scraping page {i+1}/{total_pages}: {page_url}")
                self._update_progress(vendor_id, 50 + (i * 40 / total_pages), f"Scraping page {i+1}/{total_pages}")
                
                page_content = self._fetch_url_with_curl(page_url)
                if page_content:
                    page_soup = BeautifulSoup(page_content, 'html.parser')
                    page_data = self._extract_page_content(page_soup, page_url)
                    all_content.append(page_data)
                time.sleep(1)
            
            vendor_info['pages'] = all_content
            vendor_info['total_pages_scraped'] = len(all_content)
            
            self._update_progress(vendor_id, 100, "Scraping completed successfully")
            print(f"[{vendor_id}] Scraping completed: {len(all_content)} pages scraped")
            
            return vendor_info
            
        except Exception as e:
            print(f"[{vendor_id}] Error scraping {url}: {e}")
            self._update_progress(vendor_id, 100, f"Error: {str(e)}")
            return None
    
    def _update_progress(self, vendor_id, percentage, message):
        """Update progress for a vendor."""
        if vendor_id in self.progress_callbacks:
            self.progress_callbacks[vendor_id](percentage, message)
    
    def _fetch_url_with_curl(self, url):
        """Fetch URL content using curl."""
        try:
            cmd = [
                'curl', '-s', '-L', '--max-time', '30',
                '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
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
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        vendor_name = self._extract_vendor_name(title_text, url)
        
        return {
            'url': url,
            'name': vendor_name,
            'title': title_text,
            'description': description,
            'scraped_at': time.time()
        }
    
    def _find_relevant_pages(self, soup, base_url):
        """Find all relevant pages."""
        relevant_pages = [base_url]
        
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if self._is_relevant_page(full_url, base_url):
                if full_url not in relevant_pages:
                    relevant_pages.append(full_url)
        
        return relevant_pages[:10]
    
    def _is_relevant_page(self, url, base_url):
        """Check if a page is relevant."""
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            
            if parsed_url.netloc != parsed_base.netloc:
                return False
            
            skip_patterns = [
                '/login', '/signup', '/register', '/logout',
                '/search', '/cart', '/checkout', '/account',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx',
                'javascript:', 'mailto:', 'tel:', '#'
            ]
            
            for pattern in skip_patterns:
                if pattern in url.lower():
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _extract_page_content(self, soup, url):
        """Extract content from a specific page."""
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        main_content = soup.get_text(strip=True)
        
        return {
            'url': url,
            'title': title_text,
            'content': main_content
        }
    
    def _extract_vendor_name(self, title, url):
        """Extract vendor name from title or URL."""
        if title:
            title = re.sub(r'\s*-\s*(Home|About|Services|Contact).*$', '', title, flags=re.IGNORECASE)
            return title.strip()
        
        domain = urlparse(url).netloc.replace('www.', '')
        return domain.replace('.fi', '').replace('.com', '').title()

class SimpleExtractor:
    """Simple extractor for services and products."""
    
    def __init__(self):
        pass
    
    def extract_from_raw_data(self, raw_data):
        """Extract services and products from raw scraped data."""
        try:
            result = {
                'services': [],
                'products': []
            }
            
            for page in raw_data.get('pages', []):
                page_url = page.get('url', '')
                page_title = page.get('title', '')
                page_content = page.get('content', '')
                
                if self._is_service_page(page_url, page_title):
                    service_info = {
                        'name': self._extract_service_name(page_title, page_content),
                        'category': self._extract_service_category(page_url, page_title),
                        'description': self._extract_service_description(page_content),
                        'url': page_url,
                        'pricing': self._extract_service_pricing(page_content)
                    }
                    result['services'].append(service_info)
                
                if self._is_product_page(page_url, page_title):
                    product_info = {
                        'name': self._extract_product_name(page_title, page_content),
                        'category': self._extract_product_category(page_url, page_title),
                        'description': self._extract_product_description(page_content),
                        'url': page_url,
                        'pricing': self._extract_product_pricing(page_content),
                        'target_audience': '',
                        'requirements': '',
                        'deployment': '',
                        'support': ''
                    }
                    result['products'].append(product_info)
            
            return result
            
        except Exception as e:
            print(f"Error extracting from raw data: {e}")
            return None
    
    def _is_service_page(self, url, title):
        """Determine if a page is a service page."""
        service_indicators = [
            '/services/', '/service/', '/solutions/', '/solutions-',
            'service', 'solutions', 'consulting', 'support', 'training'
        ]
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        return any(indicator in url_lower or indicator in title_lower 
                  for indicator in service_indicators)
    
    def _is_product_page(self, url, title):
        """Determine if a page is a product page."""
        product_indicators = [
            '/product/', '/products/', '/tuote/', '/solutions/',
            'product', 'solution', 'platform', 'software', 'tool'
        ]
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        return any(indicator in url_lower or indicator in title_lower 
                  for indicator in product_indicators)
    
    def _extract_service_name(self, title, content):
        """Extract service name from page title and content."""
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_service_description(self, content):
        """Extract service description from content."""
        desc_patterns = [
            r'([^.]{50,200}\.)',
            r'([A-Z][^.]{30,150}\.)'
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        return content[:200].strip() + '...' if len(content) > 200 else content.strip()
    
    def _extract_service_pricing(self, content):
        """Extract service pricing from content."""
        price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day|user|seat))?', re.IGNORECASE)
        prices = price_pattern.findall(content)
        return prices[0] if prices else None
    
    def _extract_service_category(self, url, title):
        """Extract service category from URL and title."""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'consulting' in url_lower or 'consulting' in title_lower:
            return 'consulting'
        elif 'training' in url_lower or 'training' in title_lower:
            return 'training'
        elif 'support' in url_lower or 'support' in title_lower:
            return 'support'
        elif 'security' in url_lower or 'security' in title_lower:
            return 'security'
        elif 'cloud' in url_lower or 'cloud' in title_lower:
            return 'cloud'
        else:
            return 'general'
    
    def _extract_product_name(self, title, content):
        """Extract product name from page title and content."""
        clean_title = re.sub(r'\s*-\s*.*$', '', title)
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        return clean_title.strip()
    
    def _extract_product_description(self, content):
        """Extract product description from content."""
        desc_patterns = [
            r'([^.]{50,300}\.)',
            r'([A-Z][^.]{30,200}\.)'
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0].strip()
        
        return content[:300].strip() + '...' if len(content) > 300 else content.strip()
    
    def _extract_product_pricing(self, content):
        """Extract product pricing from content."""
        price_pattern = re.compile(r'[\$€£¥]\s*[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|hour|day|user|seat))?', re.IGNORECASE)
        prices = price_pattern.findall(content)
        return prices[0] if prices else None
    
    def _extract_product_category(self, url, title):
        """Extract product category from URL and title."""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if 'security' in url_lower or 'security' in title_lower:
            return 'security'
        elif 'cloud' in url_lower or 'cloud' in title_lower:
            return 'cloud'
        elif 'software' in url_lower or 'software' in title_lower:
            return 'software'
        elif 'platform' in url_lower or 'platform' in title_lower:
            return 'platform'
        else:
            return 'general'

class SimpleWebHandler(http.server.BaseHTTPRequestHandler):
    """Simple web handler for the vendor research system."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = SimpleVendorDB()
        self.scraper = SimpleScraper()
        self.extractor = SimpleExtractor()
        self.scraping_progress = {}
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/admin':
            self.serve_admin()
        elif self.path == '/chat':
            self.serve_chat()
        elif self.path.startswith('/vendor/'):
            vendor_id = int(self.path.split('/')[-1])
            self.serve_vendor_detail(vendor_id)
        elif self.path == '/api/vendors':
            self.api_get_vendors()
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/raw-data'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_get_raw_data(vendor_id)
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/services'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_get_services(vendor_id)
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/products'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_get_products(vendor_id)
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/progress'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_get_progress(vendor_id)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/vendors':
            self.api_add_vendor()
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/scrape'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_scrape_vendor(vendor_id)
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/extract'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_extract_vendor(vendor_id)
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/remove'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_remove_vendor(vendor_id)
        elif self.path == '/api/chat':
            self.api_chat()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        """Serve the dashboard page."""
        vendors = self.db.get_vendors()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vendor Research Dashboard</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }}
                .header {{ 
                    background: #2d2d2d; 
                    padding: 20px; 
                    border-radius: 5px; 
                    border: 1px solid #444;
                }}
                .vendor-card {{ 
                    border: 1px solid #444; 
                    margin: 10px 0; 
                    padding: 15px; 
                    border-radius: 5px; 
                    background-color: #2d2d2d;
                }}
                .status {{ 
                    padding: 5px 10px; 
                    border-radius: 3px; 
                    color: white; 
                    font-size: 0.8em;
                }}
                .status.pending {{ background: #6c757d; }}
                .status.scraping {{ background: #ffc107; color: #000; }}
                .status.scraped {{ background: #28a745; }}
                .status.failed {{ background: #dc3545; }}
                .status.completed {{ background: #17a2b8; }}
                .btn {{ 
                    padding: 8px 16px; 
                    margin: 5px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    border: none;
                    cursor: pointer;
                }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-success {{ background: #28a745; color: white; }}
                .btn-info {{ background: #17a2b8; color: white; }}
                .progress-bar {{ 
                    width: 100%; 
                    height: 20px; 
                    background-color: #444; 
                    border-radius: 10px; 
                    overflow: hidden; 
                    margin: 5px 0;
                }}
                .progress-fill {{ 
                    height: 100%; 
                    background-color: #007bff; 
                    transition: width 0.3s ease;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Vendor Research Dashboard</h1>
                <a href="/admin" class="btn btn-primary">Admin Panel</a>
                <a href="/chat" class="btn btn-success">Chat Interface</a>
            </div>
            
            <h2>Recent Vendors</h2>
            {self._render_vendors(vendors)}
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_admin(self):
        """Serve the admin panel."""
        vendors = self.db.get_vendors()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }}
                .form-group {{ margin: 15px 0; }}
                label {{ display: block; margin-bottom: 5px; color: #e0e0e0; }}
                input, textarea {{ 
                    width: 100%; 
                    padding: 8px; 
                    border: 1px solid #444; 
                    border-radius: 3px; 
                    background-color: #2d2d2d; 
                    color: #e0e0e0;
                }}
                .btn {{ 
                    padding: 8px 16px; 
                    margin: 5px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    cursor: pointer; 
                    border: none;
                }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-success {{ background: #28a745; color: white; }}
                .btn-info {{ background: #17a2b8; color: white; }}
                .btn-warning {{ background: #ffc107; color: #000; }}
                .btn-danger {{ background: #dc3545; color: white; }}
                .vendor-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    background-color: #2d2d2d;
                }}
                .vendor-table th, .vendor-table td {{ 
                    border: 1px solid #444; 
                    padding: 8px; 
                    text-align: left; 
                }}
                .vendor-table th {{ background-color: #3d3d3d; }}
                .status {{ 
                    padding: 5px 10px; 
                    border-radius: 3px; 
                    color: white; 
                    font-size: 0.8em;
                }}
                .status.pending {{ background: #6c757d; }}
                .status.scraping {{ background: #ffc107; color: #000; }}
                .status.scraped {{ background: #28a745; }}
                .status.failed {{ background: #dc3545; }}
                .status.completed {{ background: #17a2b8; }}
                .progress-container {{ 
                    margin: 10px 0; 
                    padding: 10px; 
                    background-color: #2d2d2d; 
                    border-radius: 5px; 
                    border: 1px solid #444;
                }}
                .progress-bar {{ 
                    width: 100%; 
                    height: 20px; 
                    background-color: #444; 
                    border-radius: 10px; 
                    overflow: hidden; 
                    margin: 5px 0;
                }}
                .progress-fill {{ 
                    height: 100%; 
                    background-color: #007bff; 
                    transition: width 0.3s ease;
                }}
                .log-container {{ 
                    max-height: 200px; 
                    overflow-y: auto; 
                    background-color: #1a1a1a; 
                    padding: 10px; 
                    border-radius: 5px; 
                    font-family: monospace; 
                    font-size: 0.8em;
                }}
            </style>
        </head>
        <body>
            <h1>Admin Panel</h1>
            <a href="/">Back to Dashboard</a>
            
            <h2>Add New Vendors</h2>
            <form id="vendorForm">
                <div class="form-group">
                    <label for="urls">Vendor URLs (one per line):</label>
                    <textarea id="urls" name="urls" rows="5" placeholder="https://example.com&#10;https://another-vendor.com&#10;https://third-vendor.com" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Add Vendors & Start Scraping</button>
            </form>
            
            <h2>Vendor Management</h2>
            {self._render_vendor_table(vendors)}
            
            <script>
                document.getElementById('vendorForm').addEventListener('submit', function(e) {{
                    e.preventDefault();
                    
                    const urls = document.getElementById('urls').value.split('\n').filter(url => url.trim());
                    
                    if (urls.length === 0) {{
                        alert('Please enter at least one URL');
                        return;
                    }}
                    
                    const data = {{ urls: urls }};
                    
                    fetch('/api/vendors', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(data)
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Vendors added and scraping started!');
                            location.reload();
                        }} else {{
                            alert('Error: ' + result.error);
                        }}
                    }})
                    .catch(error => {{
                        alert('Error: ' + error);
                    }});
                }});
                
                function extractVendor(id) {{
                    fetch(`/api/vendors/${{id}}/extract`, {{ method: 'POST' }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Extraction started!');
                            location.reload();
                        }} else {{
                            alert('Error: ' + result.error);
                        }}
                    }});
                }}
                
                function removeVendor(id) {{
                    if (confirm('Are you sure you want to remove this vendor and all its data?')) {{
                        fetch(`/api/vendors/${{id}}/remove`, {{ method: 'POST' }})
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success) {{
                                alert('Vendor removed successfully!');
                                location.reload();
                            }} else {{
                                alert('Error: ' + result.error);
                            }}
                        }});
                    }}
                }}
                
                function viewRawData(id) {{
                    window.open(`/api/vendors/${{id}}/raw-data`, '_blank');
                }}
                
                function updateProgress() {{
                    const vendors = document.querySelectorAll('.vendor-row');
                    vendors.forEach(row => {{
                        const vendorId = row.dataset.vendorId;
                        const status = row.querySelector('.status').textContent;
                        
                        if (status === 'scraping') {{
                            fetch(`/api/vendors/${{vendorId}}/progress`)
                            .then(response => response.json())
                            .then(data => {{
                                const progressContainer = row.querySelector('.progress-container');
                                if (progressContainer) {{
                                    progressContainer.innerHTML = `
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: ${{data.percentage}}%"></div>
                                        </div>
                                        <div class="log-container">${{data.logs.join('<br>')}}</div>
                                    `;
                                }}
                            }});
                        }}
                    }});
                }}
                
                // Update progress every 2 seconds
                setInterval(updateProgress, 2000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_chat(self):
        """Serve the chat interface."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chat Interface</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }
                .chat-container { 
                    border: 1px solid #444; 
                    height: 400px; 
                    overflow-y: auto; 
                    padding: 10px; 
                    margin: 10px 0; 
                    background-color: #2d2d2d;
                }
                .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .user-message { background: #007bff; text-align: right; }
                .bot-message { background: #444; }
                .input-group { display: flex; margin: 10px 0; }
                .input-group input { 
                    flex: 1; 
                    padding: 8px; 
                    border: 1px solid #444; 
                    border-radius: 3px; 
                    background-color: #2d2d2d; 
                    color: #e0e0e0;
                }
                .btn { 
                    padding: 8px 16px; 
                    margin: 5px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    cursor: pointer; 
                    border: none;
                }
                .btn-primary { background: #007bff; color: white; }
            </style>
        </head>
        <body>
            <h1>Chat Interface</h1>
            <a href="/">Back to Dashboard</a>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    <strong>System:</strong> Hello! I can help you query the vendor database. Try asking questions like:
                    <ul>
                        <li>Which vendors offer cybersecurity services?</li>
                        <li>What products are available for endpoint security?</li>
                        <li>Show me vendors with cloud solutions</li>
                    </ul>
                </div>
            </div>
            
            <div class="input-group">
                <input type="text" id="chatInput" placeholder="Ask about vendors, services, or products...">
                <button class="btn btn-primary" onclick="sendMessage()">Send</button>
            </div>
            
            <script>
                function sendMessage() {
                    const input = document.getElementById('chatInput');
                    const message = input.value.trim();
                    
                    if (!message) return;
                    
                    const chatContainer = document.getElementById('chatContainer');
                    chatContainer.innerHTML += `<div class="message user-message"><strong>You:</strong> ${message}</div>`;
                    
                    chatContainer.innerHTML += `<div class="message bot-message"><strong>Assistant:</strong> Thinking...</div>`;
                    
                    input.value = '';
                    
                    fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({query: message})
                    })
                    .then(response => response.json())
                    .then(result => {
                        const messages = document.querySelectorAll('.message');
                        const lastMessage = messages[messages.length - 1];
                        lastMessage.innerHTML = `<strong>Assistant:</strong> ${result.response}`;
                    })
                    .catch(error => {
                        const messages = document.querySelectorAll('.message');
                        const lastMessage = messages[messages.length - 1];
                        lastMessage.innerHTML = `<strong>Assistant:</strong> Error: ${error}`;
                    });
                }
                
                document.getElementById('chatInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_vendor_detail(self, vendor_id):
        """Serve vendor detail page."""
        vendor = self.db.get_vendor(vendor_id)
        if not vendor:
            self.send_error(404)
            return
        
        services = self.db.get_vendor_services(vendor_id)
        products = self.db.get_vendor_products(vendor_id)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{vendor[1]} - Vendor Details</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }}
                .vendor-info {{ 
                    border: 1px solid #444; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 5px; 
                    background-color: #2d2d2d;
                }}
                .service-card, .product-card {{ 
                    border: 1px solid #444; 
                    margin: 10px 0; 
                    padding: 15px; 
                    border-radius: 5px; 
                    background-color: #2d2d2d;
                }}
                .status {{ 
                    padding: 5px 10px; 
                    border-radius: 3px; 
                    color: white; 
                    font-size: 0.8em;
                }}
                .status.pending {{ background: #6c757d; }}
                .status.scraping {{ background: #ffc107; color: #000; }}
                .status.scraped {{ background: #28a745; }}
                .status.failed {{ background: #dc3545; }}
                .status.completed {{ background: #17a2b8; }}
            </style>
        </head>
        <body>
            <h1>{vendor[1]}</h1>
            <a href="/admin">Back to Admin Panel</a>
            
            <div class="vendor-info">
                <h2>Vendor Information</h2>
                <p><strong>Website:</strong> <a href="{vendor[2]}" target="_blank">{vendor[2]}</a></p>
                <p><strong>Status:</strong> <span class="status {vendor[4]}">{vendor[4]}</span></p>
                <p><strong>Description:</strong> {vendor[3] or 'No description available'}</p>
                <p><strong>Scraped:</strong> {vendor[6] or 'Not scraped yet'}</p>
            </div>
            
            <div class="services">
                <h2>Services</h2>
                {self._render_services(services)}
            </div>
            
            <div class="products">
                <h2>Products</h2>
                {self._render_products(products)}
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def api_add_vendor(self):
        """API endpoint to add vendors."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        urls = data.get('urls', [])
        if not urls:
            response = {'error': 'No URLs provided'}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        vendor_ids = []
        for url in urls:
            url = url.strip()
            if url:
                # Extract vendor name from URL
                domain = urlparse(url).netloc.replace('www.', '')
                vendor_name = domain.replace('.fi', '').replace('.com', '').title()
                
                vendor_id = self.db.add_vendor(vendor_name, url, '')
                vendor_ids.append(vendor_id)
                
                # Start scraping immediately
                self._start_scraping(vendor_id, url)
        
        response = {'success': True, 'vendor_ids': vendor_ids, 'message': f'Added {len(vendor_ids)} vendors and started scraping'}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_remove_vendor(self, vendor_id):
        """API endpoint to remove a vendor."""
        success = self.db.remove_vendor(vendor_id)
        
        if success:
            response = {'success': True, 'message': 'Vendor removed successfully'}
        else:
            response = {'error': 'Vendor not found'}
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _start_scraping(self, vendor_id, url):
        """Start scraping for a vendor."""
        self.db.update_vendor_status(vendor_id, 'scraping')
        
        # Initialize progress tracking
        self.scraping_progress[vendor_id] = {
            'percentage': 0,
            'logs': []
        }
        
        def progress_callback(percentage, message):
            self.scraping_progress[vendor_id]['percentage'] = percentage
            self.scraping_progress[vendor_id]['logs'].append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            # Keep only last 50 log entries
            if len(self.scraping_progress[vendor_id]['logs']) > 50:
                self.scraping_progress[vendor_id]['logs'] = self.scraping_progress[vendor_id]['logs'][-50:]
        
        self.scraper.set_progress_callback(vendor_id, progress_callback)
        
        def scrape_worker():
            try:
                result = self.scraper.scrape_vendor(vendor_id, url)
                
                if result:
                    self.db.update_vendor_status(vendor_id, 'scraped', json.dumps(result))
                else:
                    self.db.update_vendor_status(vendor_id, 'failed')
                
                # Clean up progress tracking after completion
                if vendor_id in self.scraping_progress:
                    del self.scraping_progress[vendor_id]
                
            except Exception as e:
                print(f"Error scraping vendor {vendor_id}: {e}")
                self.db.update_vendor_status(vendor_id, 'failed')
                if vendor_id in self.scraping_progress:
                    del self.scraping_progress[vendor_id]
        
        thread = threading.Thread(target=scrape_worker)
        thread.start()
    
    def api_get_vendors(self):
        """API endpoint to get all vendors."""
        vendors = self.db.get_vendors()
        vendors_data = []
        
        for vendor in vendors:
            vendors_data.append({
                'id': vendor[0],
                'name': vendor[1],
                'website': vendor[2],
                'description': vendor[3],
                'status': vendor[4],
                'scraped_at': vendor[6],
                'created_at': vendor[7]
            })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(vendors_data).encode())
    
    def api_scrape_vendor(self, vendor_id):
        """API endpoint to scrape a vendor."""
        vendor = self.db.get_vendor(vendor_id)
        if not vendor:
            self.send_error(404)
            return
        
        if vendor[4] == 'scraping':
            response = {'error': 'Vendor is already being scraped'}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self._start_scraping(vendor_id, vendor[2])
        
        response = {'success': True, 'message': 'Scraping started'}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_get_progress(self, vendor_id):
        """API endpoint to get scraping progress."""
        if vendor_id in self.scraping_progress:
            progress_data = self.scraping_progress[vendor_id]
        else:
            progress_data = {'percentage': 100, 'logs': ['Scraping completed']}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(progress_data).encode())
    
    def api_extract_vendor(self, vendor_id):
        """API endpoint to extract services and products from a vendor."""
        vendor = self.db.get_vendor(vendor_id)
        if not vendor:
            self.send_error(404)
            return
        
        if not vendor[5]:
            response = {'error': 'No scraped data available'}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        def extract_worker():
            try:
                raw_data = json.loads(vendor[5])
                result = self.extractor.extract_from_raw_data(raw_data)
                
                if result:
                    for service_data in result.get('services', []):
                        self.db.add_service(
                            vendor_id,
                            service_data['name'],
                            service_data.get('category', ''),
                            service_data.get('description', ''),
                            service_data.get('url', ''),
                            service_data.get('pricing', '')
                        )
                    
                    for product_data in result.get('products', []):
                        self.db.add_product(
                            vendor_id,
                            product_data['name'],
                            product_data.get('category', ''),
                            product_data.get('description', ''),
                            product_data.get('url', ''),
                            product_data.get('pricing', ''),
                            product_data.get('target_audience', ''),
                            product_data.get('requirements', ''),
                            product_data.get('deployment', ''),
                            product_data.get('support', '')
                        )
                    
                    self.db.update_vendor_status(vendor_id, 'completed')
                else:
                    self.db.update_vendor_status(vendor_id, 'failed')
                
            except Exception as e:
                print(f"Error extracting vendor {vendor_id}: {e}")
                self.db.update_vendor_status(vendor_id, 'failed')
        
        thread = threading.Thread(target=extract_worker)
        thread.start()
        
        response = {'success': True, 'message': 'Extraction started'}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_get_raw_data(self, vendor_id):
        """API endpoint to get raw scraped data."""
        vendor = self.db.get_vendor(vendor_id)
        if not vendor or not vendor[5]:
            self.send_error(404)
            return
        
        raw_data = json.loads(vendor[5])
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(raw_data, indent=2).encode())
    
    def api_get_services(self, vendor_id):
        """API endpoint to get vendor services."""
        services = self.db.get_vendor_services(vendor_id)
        services_data = []
        
        for service in services:
            services_data.append({
                'id': service[0],
                'name': service[2],
                'category': service[3],
                'description': service[4],
                'url': service[5],
                'pricing': service[6]
            })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(services_data).encode())
    
    def api_get_products(self, vendor_id):
        """API endpoint to get vendor products."""
        products = self.db.get_vendor_products(vendor_id)
        products_data = []
        
        for product in products:
            products_data.append({
                'id': product[0],
                'name': product[2],
                'category': product[3],
                'description': product[4],
                'url': product[5],
                'pricing': product[6],
                'target_audience': product[7],
                'requirements': product[8],
                'deployment': product[9],
                'support': product[10]
            })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(products_data).encode())
    
    def api_chat(self):
        """API endpoint for chat queries."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        query = data.get('query', '')
        
        # Simple text search for now
        vendors = self.db.get_vendors()
        response_text = "Here's what I found:\n\n"
        
        found_results = False
        
        for vendor in vendors:
            if query.lower() in vendor[1].lower() or query.lower() in (vendor[3] or '').lower():
                response_text += f"**Vendor**: {vendor[1]}\n"
                response_text += f"Website: {vendor[2]}\n"
                response_text += f"Status: {vendor[4]}\n\n"
                found_results = True
        
        if not found_results:
            response_text = "No relevant information found. Try searching for specific vendor names or descriptions."
        
        response = {'response': response_text}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _render_vendors(self, vendors):
        """Render vendors list."""
        if not vendors:
            return "<p>No vendors added yet. Go to Admin Panel to add vendors.</p>"
        
        html = ""
        for vendor in vendors[:5]:  # Show only first 5
            status_class = vendor[4]
            html += f"""
            <div class="vendor-card">
                <h3>{vendor[1]}</h3>
                <p>{vendor[2]}</p>
                <span class="status {status_class}">{status_class}</span>
                <a href="/vendor/{vendor[0]}" class="btn btn-info">View Details</a>
            </div>
            """
        return html
    
    def _render_vendor_table(self, vendors):
        """Render vendor management table."""
        if not vendors:
            return "<p>No vendors added yet. Add vendors using the form above.</p>"
        
        html = """
        <table class="vendor-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for vendor in vendors:
            html += f"""
            <tr class="vendor-row" data-vendor-id="{vendor[0]}">
                <td><a href="/vendor/{vendor[0]}" style="color: #007bff;">{vendor[1]}</a></td>
                <td><span class="status {vendor[4]}">{vendor[4]}</span></td>
                <td>
            """
            
            if vendor[4] == 'scraped':
                html += f'<button class="btn btn-success" onclick="extractVendor({vendor[0]})">Extract</button>'
            
            html += f'<button class="btn btn-info" onclick="viewRawData({vendor[0]})">Raw Data</button>'
            html += f'<button class="btn btn-danger" onclick="removeVendor({vendor[0]})">Remove</button>'
            html += "</td></tr>"
            
            # Add progress container for scraping vendors
            if vendor[4] == 'scraping':
                html += f"""
                <tr class="vendor-row" data-vendor-id="{vendor[0]}">
                    <td colspan="3">
                        <div class="progress-container">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 0%"></div>
                            </div>
                            <div class="log-container">Starting...</div>
                        </div>
                    </td>
                </tr>
                """
        
        html += "</tbody></table>"
        return html
    
    def _render_services(self, services):
        """Render services list."""
        if not services:
            return "<p>No services extracted yet. Run extraction to get detailed service information.</p>"
        
        html = ""
        for service in services:
            html += f"""
            <div class="service-card">
                <h3>{service[2]}</h3>
                <p><strong>Category:</strong> {service[3] or 'N/A'}</p>
                <p><strong>Description:</strong> {service[4] or 'No description available'}</p>
                <p><strong>Pricing:</strong> {service[6] or 'No pricing information'}</p>
                {f'<p><strong>URL:</strong> <a href="{service[5]}" target="_blank" style="color: #007bff;">{service[5]}</a></p>' if service[5] else ''}
            </div>
            """
        return html
    
    def _render_products(self, products):
        """Render products list."""
        if not products:
            return "<p>No products extracted yet. Run extraction to get detailed product information.</p>"
        
        html = ""
        for product in products:
            html += f"""
            <div class="product-card">
                <h3>{product[2]}</h3>
                <p><strong>Category:</strong> {product[3] or 'N/A'}</p>
                <p><strong>Description:</strong> {product[4] or 'No description available'}</p>
                <p><strong>Pricing:</strong> {product[6] or 'No pricing information'}</p>
                {f'<p><strong>URL:</strong> <a href="{product[5]}" target="_blank" style="color: #007bff;">{product[5]}</a></p>' if product[5] else ''}
            </div>
            """
        return html

def find_free_port():
    """Find a free port to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Main function to start the web server."""
    # Try to find a free port
    PORT = find_free_port()
    
    print(f"Starting Vendor Research Web Server on port {PORT}")
    print(f"Access the application at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    print(f"Chat Interface: http://localhost:{PORT}/chat")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleWebHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {PORT} is already in use. Trying a different port...")
            PORT = find_free_port()
            print(f"Using port {PORT} instead")
            with socketserver.TCPServer(("", PORT), SimpleWebHandler) as httpd:
                print(f"Server running on http://localhost:{PORT}")
                httpd.serve_forever()
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
