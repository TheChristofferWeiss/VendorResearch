#!/usr/bin/env python3
"""
Complete Vendor Research Server with all functionality
"""

import http.server
import socketserver
import json
import sqlite3
import socket
import threading
import time
import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time as time_module
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

class SimpleVendorDB:
    def __init__(self, db_path='vendor_research.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create vendors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                website TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                html_stored BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add html_stored column if it doesn't exist (for existing databases)
        try:
            cursor.execute('ALTER TABLE vendors ADD COLUMN html_stored BOOLEAN DEFAULT FALSE')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Add progress tracking columns
        try:
            cursor.execute('ALTER TABLE vendors ADD COLUMN pages_scraped INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute('ALTER TABLE vendors ADD COLUMN total_pages INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        
        # Create services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                service_name TEXT,
                description TEXT,
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                product_name TEXT,
                description TEXT,
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_vendor(self, name, website, description=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vendors (name, website, description)
            VALUES (?, ?, ?)
        ''', (name, website, description))
        vendor_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return vendor_id
    
    def get_vendors(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, website, description, status, html_stored, created_at, pages_scraped, total_pages FROM vendors ORDER BY created_at DESC')
        vendors = cursor.fetchall()
        conn.close()
        return vendors
    
    def remove_vendor(self, vendor_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
        cursor.execute('DELETE FROM services WHERE vendor_id = ?', (vendor_id,))
        cursor.execute('DELETE FROM products WHERE vendor_id = ?', (vendor_id,))
        conn.commit()
        conn.close()
    
    def update_vendor_status(self, vendor_id, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE vendors SET status = ? WHERE id = ?', (status, vendor_id))
        conn.commit()
        conn.close()
    
    def update_html_stored(self, vendor_id, html_stored=True):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE vendors SET html_stored = ? WHERE id = ?', (html_stored, vendor_id))
        conn.commit()
        conn.close()
    
    def update_scraping_progress(self, vendor_id, pages_scraped, total_pages):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE vendors SET pages_scraped = ?, total_pages = ? WHERE id = ?', (pages_scraped, total_pages, vendor_id))
        conn.commit()
        conn.close()
    
    def add_service(self, vendor_id, service_name, description=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO services (vendor_id, service_name, description)
            VALUES (?, ?, ?)
        ''', (vendor_id, service_name, description))
        conn.commit()
        conn.close()
    
    def add_product(self, vendor_id, product_name, description=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (vendor_id, product_name, description)
            VALUES (?, ?, ?)
        ''', (vendor_id, product_name, description))
        conn.commit()
        conn.close()

class PlaywrightScraper:
    def __init__(self):
        self.scraped_urls = set()
        self.max_pages = None  # No limit - scrape all pages
        self.playwright = None
        self.browser = None
        self.context = None
    
    def _init_browser(self):
        """Initialize Playwright browser with stealth settings - thread-safe version"""
        # Create a new browser instance for this thread to avoid threading issues
        playwright_instance = sync_playwright().start()
        browser = playwright_instance.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--disable-dev-shm-usage', '--no-sandbox', '--disable-setuid-sandbox']
        )
        # Create context with realistic browser settings
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Store thread-local instances
        self.playwright = playwright_instance
        self.browser = browser
        self.context = context
    
    def __del__(self):
        """Cleanup browser resources"""
        self.close()
    
    def close(self):
        """Close browser and cleanup"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def scrape_url(self, url):
        """Scrape a single URL using curl (thread-safe)"""
        try:
            # Use curl with browser-like headers to avoid detection
            cmd = [
                'curl', '-s', '-L', '--compressed',  # --compressed tells curl to decompress gzip automatically
                '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                '-H', 'Accept-Language: en-US,en;q=0.9',
                '-H', 'Accept-Encoding: gzip, deflate, br',
                '-H', 'DNT: 1',
                '-H', 'Connection: keep-alive',
                '-H', 'Upgrade-Insecure-Requests: 1',
                '-H', 'Sec-Fetch-Dest: document',
                '-H', 'Sec-Fetch-Mode: navigate',
                '-H', 'Sec-Fetch-Site: none',
                '-H', 'Sec-Fetch-User: ?1',
                '-H', 'Cache-Control: max-age=0',
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Check if we got an access denied or blocked page (be very specific)
                content_lower = result.stdout.lower()
                # Only check for actual blocking messages, not general keywords
                blocking_phrases = [
                    "your request was blocked",
                    "access denied by administrator",
                    "403 forbidden",
                    "cloudflare ray id",
                    "you have been blocked",
                    "unauthorized access"
                ]
                if any(phrase in content_lower for phrase in blocking_phrases):
                    print(f"Access denied or blocked for {url}")
                    return None
                
                # Use trafilatura to extract clean content
                html_content = result.stdout
                clean_content = self._extract_with_trafilatura(html_content)
                
                if clean_content:
                    # Check if content is too short or contains placeholder text
                    if len(clean_content.strip()) < 50 or "# Index" in clean_content:
                        print(f"Skipping {url}: content too short or placeholder")
                        return None
                    return clean_content
                else:
                    # Check raw HTML for placeholder content
                    if "# Index" in html_content:
                        print(f"Skipping {url}: placeholder content")
                        return None
                    return html_content
            else:
                print(f"Curl error for {url}: {result.stderr}")
                return None
        except UnicodeDecodeError as e:
            print(f"Unicode decode error for {url}: {e}")
            # Try again without text=True to get raw bytes
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                if result.returncode == 0:
                    # Try to decode with different encodings
                    content = result.stdout
                    try:
                        html_content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            html_content = content.decode('latin-1')
                        except UnicodeDecodeError:
                            html_content = content.decode('utf-8', errors='ignore')
                    
                    # Use trafilatura on the decoded content
                    clean_content = self._extract_with_trafilatura(html_content)
                    if clean_content:
                        # Check if content is valid
                        if len(clean_content.strip()) < 50 or "# Index" in clean_content:
                            return None
                        return clean_content
                    # Check raw HTML for placeholder content
                    if "# Index" in html_content:
                        return None
                    return html_content
                return None
            except Exception as e2:
                print(f"Error scraping {url} (retry): {e2}")
                return None
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def _extract_with_trafilatura(self, html_content):
        """Extract clean content using trafilatura"""
        try:
            import trafilatura
            from trafilatura import extract
            
            # Extract clean text content
            clean_text = extract(html_content)
            
            if clean_text and len(clean_text.strip()) > 100:
                return clean_text
            else:
                print("Trafilatura extraction returned minimal content")
                return None
                
        except ImportError:
            print("Trafilatura not available, using fallback extraction")
            return None
        except Exception as e:
            print(f"Trafilatura error: {e}")
            return None
    
    def scrape_entire_site(self, base_url, progress_callback=None, save_callback=None):
        """Scrape entire website using curl"""
        try:
            print(f"Starting to scrape entire site: {base_url}")
            all_urls = self._discover_site_urls(base_url)
            filtered_urls = [url for url in all_urls if not self._is_blog_url(url) and not self._is_legal_page(url) and self._is_english_page(url) and self._is_products_or_services_page(url)]
            print(f"Found {len(filtered_urls)} English Product/Service pages to scrape")
            
            # Slice URLs if max_pages is set, otherwise scrape all
            urls_to_scrape = filtered_urls[:self.max_pages] if self.max_pages else filtered_urls
            total_pages = len(urls_to_scrape)
            
            all_content = []
            for i, url in enumerate(urls_to_scrape):
                print(f"Scraping page {i+1}/{total_pages}: {url}")
                content = self.scrape_url(url)
                if content:
                    page_data = {'url': url, 'content': content, 'index': i+1}
                    all_content.append(page_data)
                    
                    # Save immediately if callback provided
                    if save_callback:
                        save_callback(page_data)
                
                # Update progress
                if progress_callback:
                    progress_callback(len(all_content), total_pages)
                
                time_module.sleep(1)
            
            print(f"Successfully scraped {len(all_content)} pages")
            return all_content
        except Exception as e:
            print(f"Error scraping entire site {base_url}: {e}")
            return []
    
    def _discover_site_urls(self, base_url):
        """Discover all URLs using curl"""
        try:
            from urllib.parse import urljoin
            # Use curl to get HTML
            cmd = ['curl', '-s', '-L', base_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                return [base_url]
            
            html_content = result.stdout
            urls = set([base_url])
            
            # Parse HTML to find links
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    # Only include URLs from the same domain
                    if urlparse(base_url).netloc in urlparse(href).netloc:
                        full_url = href
                    else:
                        continue
                else:
                    continue
                
                # Clean URL
                clean_url = full_url.split('#')[0].split('?')[0]
                urls.add(clean_url)
            
            return list(urls)
        except Exception as e:
            print(f"Error discovering URLs for {base_url}: {e}")
            return [base_url]
    
    def _is_blog_url(self, url):
        blog_keywords = ['blog', 'news', 'article', 'post', 'press-release']
        return any(keyword in url.lower() for keyword in blog_keywords)
    
    def _is_legal_page(self, url):
        legal_keywords = ['privacy-policy', 'privacy_policy', 'privacy', 'terms-of-use', 'terms_of_use', 'terms', 'accessibility-statement', 'accessibility_statement', 'accessibility', 'cookie-policy', 'cookie_policy', 'cookies', 'legal', 'disclaimer', 'sitemap', 'contact-us', 'contact_us', 'contact']
        return any(keyword in url.lower() for keyword in legal_keywords)
    
    def _is_english_page(self, url):
        non_english_codes = ['/de/', '/fr/', '/es/', '/it/', '/pt/', '/ru/', '/ja/', '/ko/', '/zh/', '/ar/', '/sv/', '/no/', '/fi/', '/nl/', '/da/', '/pl/', '/cs/', '/hu/', '/ro/', '/bg/', '/hr/', '/sk/', '/sl/', '/et/', '/lv/', '/lt/', '/el/', '/tr/', '/he/', '/th/', '/vi/', '/id/', '/ms/', '/tl/']
        return not any(code in url.lower() for code in non_english_codes)
    
    def _is_products_or_services_page(self, url):
        """Check if URL is a Products or Services page"""
        url_lower = url.lower()
        return '/products/' in url_lower or '/services/' in url_lower or '/solutions/' in url_lower

class SimpleExtractor:
    def __init__(self):
        pass
    
    def extract_services_products(self, content):
        if not content:
            return [], []
        
        try:
            # If content is already clean text from trafilatura, use it directly
            if not content.strip().startswith('<'):
                # This is clean text, not HTML
                return self._extract_from_clean_text(content)
            
            # Otherwise, parse as HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            return self._extract_from_clean_text(text)
            
        except Exception as e:
            print(f"Error extracting content: {e}")
            return [], []
    
    def _extract_from_clean_text(self, text):
        """Extract services and products from clean text content"""
        try:
            services = []
            products = []
            
            # Split text into sentences/paragraphs
            sentences = text.split('.')
            
            # Look for service-related keywords
            service_keywords = ['service', 'solution', 'platform', 'software', 'tool', 'system', 'offering', 'capability']
            product_keywords = ['product', 'software', 'app', 'tool', 'platform', 'solution', 'feature', 'module']
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 20 or len(sentence) > 300:
                    continue
                
                sentence_lower = sentence.lower()
                
                # Check for service indicators
                if any(keyword in sentence_lower for keyword in service_keywords):
                    # Look for service names (usually capitalized)
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if word.lower() in service_keywords and i > 0:
                            # Get surrounding context
                            start = max(0, i-2)
                            end = min(len(words), i+3)
                            service_text = ' '.join(words[start:end])
                            if len(service_text) > 10 and len(service_text) < 150:
                                services.append(service_text.strip())
                
                # Check for product indicators
                if any(keyword in sentence_lower for keyword in product_keywords):
                    # Look for product names
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if word.lower() in product_keywords and i > 0:
                            # Get surrounding context
                            start = max(0, i-2)
                            end = min(len(words), i+3)
                            product_text = ' '.join(words[start:end])
                            if len(product_text) > 10 and len(product_text) < 150:
                                products.append(product_text.strip())
            
            # Remove duplicates and limit results
            services = list(set(services))[:15]
            products = list(set(products))[:15]
            
            return services, products
            
        except Exception as e:
            print(f"Error extracting from clean text: {e}")
            return [], []

class SimpleWebHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = SimpleVendorDB()
        self.scraper = PlaywrightScraper()
        self.extractor = SimpleExtractor()
        self.scraping_progress = {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(f"GET request for: {self.path}")
        
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/admin':
            self.serve_admin()
        elif self.path == '/api/vendors/progress':
            self.api_get_progress()
        elif self.path.startswith('/api/vendors/'):
            self.handle_vendor_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        print(f"POST request for: {self.path}")
        
        if self.path == '/api/vendors':
            self.api_add_vendor()
        elif self.path.startswith('/api/vendors/'):
            self.handle_vendor_api()
        else:
            self.send_error(404)
    
    def handle_vendor_api(self):
        if self.path.endswith('/remove'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_remove_vendor(vendor_id)
        elif self.path.endswith('/scrape'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_scrape_vendor(vendor_id)
        elif self.path.endswith('/extract'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_extract_vendor(vendor_id)
        elif self.path.endswith('/progress'):
            self.api_get_progress()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
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
                .btn {{ 
                    padding: 8px 16px; 
                    margin: 5px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    cursor: pointer; 
                    border: none;
                }}
                .btn-primary {{ background: #007bff; color: white; }}
                .btn-danger {{ background: #dc3545; color: white; }}
                .btn-success {{ background: #28a745; color: white; }}
                .btn-warning {{ background: #ffc107; color: black; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Vendor Research Dashboard</h1>
                <p>Manage and research vendors</p>
                <a href="/admin" class="btn btn-primary">Admin Panel</a>
            </div>
            
            <h2>Vendors ({len(vendors)})</h2>
            {self._render_vendors(vendors)}
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_admin(self):
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
                .btn-danger {{ background: #dc3545; color: white; }}
                .btn-success {{ background: #28a745; color: white; }}
                .btn-warning {{ background: #ffc107; color: black; }}
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
                .progress-container {{
                    position: relative;
                    width: 100%;
                    height: 20px;
                    background-color: #1a1a1a;
                    border-radius: 3px;
                    overflow: hidden;
                }}
                .progress-bar {{
                    height: 100%;
                    background-color: #28a745;
                    transition: width 0.3s ease;
                }}
                .progress-text {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 11px;
                    color: #e0e0e0;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Admin Panel</h1>
            
            <h2>Add Vendor</h2>
            <form id="addVendorForm">
                <div class="form-group">
                    <label for="urls">Vendor URLs (one per line):</label>
                    <textarea id="urls" name="urls" rows="5" placeholder="https://example.com"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Add Vendors</button>
            </form>
            
            <h2>Vendors ({len(vendors)})</h2>
            <div style="margin-bottom: 15px;">
                <button class="btn btn-success" onclick="selectAllVendors()">Select All</button>
                <button class="btn btn-warning" onclick="extractSelectedVendors()">Extract Selected</button>
                <button class="btn btn-primary" onclick="extractAllVendors()">Extract All</button>
            </div>
            <table class="vendor-table">
                <thead>
                    <tr>
                        <th><input type="checkbox" id="selectAllCheckbox" onchange="toggleAllVendors()"></th>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Website</th>
                        <th>Status</th>
                        <th>Progress</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {self._render_vendor_table(vendors)}
                </tbody>
            </table>
            
            <script>
                document.getElementById('addVendorForm').addEventListener('submit', function(e) {{
                    e.preventDefault();
                    
                    const urls = document.getElementById('urls').value;
                    if (!urls.trim()) {{
                        alert('Please enter at least one URL');
                        return;
                    }}
                    
                    fetch('/api/vendors', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify({{ urls: urls }})
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            location.reload();
                        }} else {{
                            alert('Error: ' + result.error);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                        alert('Error adding vendors: ' + error.message);
                    }});
                }});
                
                function removeVendor(vendorId) {{
                    if (confirm('Are you sure you want to remove this vendor?')) {{
                        fetch(`/api/vendors/${{vendorId}}/remove`, {{
                            method: 'POST'
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success) {{
                                location.reload();
                            }} else {{
                                alert('Error: ' + result.error);
                            }}
                        }})
                        .catch(error => {{
                            console.error('Error:', error);
                            alert('Error removing vendor: ' + error.message);
                        }});
                    }}
                }}
                
                function scrapeVendor(vendorId) {{
                    fetch(`/api/vendors/${{vendorId}}/scrape`, {{
                        method: 'POST'
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Scraping started!');
                            location.reload();
                        }} else {{
                            alert('Error: ' + result.error);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                        alert('Error starting scraping: ' + error.message);
                    }});
                }}
                
                function extractVendor(vendorId) {{
                    fetch(`/api/vendors/${{vendorId}}/extract`, {{
                        method: 'POST'
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Extraction started!');
                            location.reload();
                        }} else {{
                            alert('Error: ' + result.error);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                        alert('Error starting extraction: ' + error.message);
                    }});
                }}
                
                function selectAllVendors() {{
                    const checkboxes = document.querySelectorAll('.vendor-checkbox');
                    checkboxes.forEach(checkbox => checkbox.checked = true);
                    document.getElementById('selectAllCheckbox').checked = true;
                }}
                
                function toggleAllVendors() {{
                    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
                    const checkboxes = document.querySelectorAll('.vendor-checkbox');
                    checkboxes.forEach(checkbox => checkbox.checked = selectAllCheckbox.checked);
                }}
                
                function extractSelectedVendors() {{
                    const checkboxes = document.querySelectorAll('.vendor-checkbox:checked');
                    if (checkboxes.length === 0) {{
                        alert('Please select at least one vendor to extract');
                        return;
                    }}
                    
                    const vendorIds = Array.from(checkboxes).map(checkbox => checkbox.value);
                    
                    // Start extraction for each selected vendor
                    vendorIds.forEach(vendorId => {{
                        fetch(`/api/vendors/${{vendorId}}/extract`, {{
                            method: 'POST'
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (!result.success) {{
                                console.error('Error extracting vendor', vendorId, ':', result.error);
                            }}
                        }})
                        .catch(error => {{
                            console.error('Error extracting vendor', vendorId, ':', error);
                        }});
                    }});
                    
                    alert(`Started extraction for ${{vendorIds.length}} vendors`);
                    location.reload();
                }}
                
                function extractAllVendors() {{
                    const checkboxes = document.querySelectorAll('.vendor-checkbox');
                    if (checkboxes.length === 0) {{
                        alert('No vendors found');
                        return;
                    }}
                    
                    if (!confirm(`Extract all ${{checkboxes.length}} vendors?`)) {{
                        return;
                    }}
                    
                    const vendorIds = Array.from(checkboxes).map(checkbox => checkbox.value);
                    
                    // Start extraction for each vendor
                    vendorIds.forEach(vendorId => {{
                        fetch(`/api/vendors/${{vendorId}}/extract`, {{
                            method: 'POST'
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (!result.success) {{
                                console.error('Error extracting vendor', vendorId, ':', result.error);
                            }}
                        }})
                        .catch(error => {{
                            console.error('Error extracting vendor', vendorId, ':', error);
                        }});
                    }});
                    
                    alert(`Started extraction for all ${{vendorIds.length}} vendors`);
                    location.reload();
                }}
                
                // Poll for progress updates
                function updateProgress() {{
                    fetch('/api/vendors/progress')
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success && result.progress) {{
                                for (const [vendorId, progress] of Object.entries(result.progress)) {{
                                    const row = document.querySelector(`tr[data-vendor-id="${{vendorId}}"]`);
                                    if (row) {{
                                        const progressCell = row.cells[5];
                                        if (progressCell) {{
                                            const percentage = progress.percentage;
                                            progressCell.innerHTML = `
                                                <div class="progress-container">
                                                    <div class="progress-bar" style="width: ${{percentage}}%"></div>
                                                    <span class="progress-text">${{progress.pages_scraped}}/${{progress.total_pages}}</span>
                                                </div>
                                            `;
                                        }}
                                    }}
                                }}
                            }}
                        }})
                        .catch(error => console.error('Error fetching progress:', error));
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
    
    def _render_vendors(self, vendors):
        if not vendors:
            return "<p>No vendors found.</p>"
        
        html = ""
        for vendor in vendors:
            html += f"""
            <div class="vendor-card">
                <h3>{vendor[1]}</h3>
                <p><strong>Website:</strong> <a href="{vendor[2]}" target="_blank">{vendor[2]}</a></p>
                <p><strong>Status:</strong> {vendor[4]}</p>
                {f'<p><strong>Description:</strong> {vendor[3]}</p>' if vendor[3] else ''}
                <div>
                    <button class="btn btn-success" onclick="scrapeVendor({vendor[0]})">Scrape</button>
                    <button class="btn btn-warning" onclick="extractVendor({vendor[0]})">Extract</button>
                    <button class="btn btn-danger" onclick="removeVendor({vendor[0]})">Remove</button>
                </div>
            </div>
            """
        return html
    
    def _render_vendor_table(self, vendors):
        if not vendors:
            return "<tr><td colspan='7'>No vendors found.</td></tr>"
        
        html = ""
        for vendor in vendors:
            # vendor structure: id, name, website, description, status, html_stored, created_at, pages_scraped, total_pages
            vendor_id = vendor[0]
            pages_scraped = vendor[7] if len(vendor) > 7 else 0
            total_pages = vendor[8] if len(vendor) > 8 else 0
            percentage = int((pages_scraped / total_pages * 100)) if total_pages > 0 else 0
            
            progress_bar = f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {percentage}%"></div>
                    <span class="progress-text">{pages_scraped}/{total_pages}</span>
                </div>
            """ if vendor[4] == 'scraping' else ""
            
            html += f"""
            <tr data-vendor-id="{vendor_id}">
                <td><input type="checkbox" class="vendor-checkbox" value="{vendor_id}"></td>
                <td>{vendor_id}</td>
                <td>{vendor[1]}</td>
                <td><a href="{vendor[2]}" target="_blank">{vendor[2]}</a></td>
                <td>{vendor[4]}</td>
                <td>{progress_bar}</td>
                <td>
                    <button class="btn btn-success" onclick="scrapeVendor({vendor_id})">Scrape</button>
                    <button class="btn btn-warning" onclick="extractVendor({vendor_id})">Extract</button>
                    <button class="btn btn-danger" onclick="removeVendor({vendor_id})">Remove</button>
                </td>
            </tr>
            """
        return html
    
    def api_add_vendor(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        urls = data.get('urls', '').strip()
        if not urls:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No URLs provided'}).encode())
            return
        
        url_list = [url.strip() for url in urls.split('\n') if url.strip()]
        vendor_ids = []
        
        for url in url_list:
            try:
                domain = urlparse(url).netloc
                vendor_id = self.db.add_vendor(domain, url, f"Vendor from {domain}")
                vendor_ids.append(vendor_id)
                
                # Start scraping in background
                threading.Thread(target=self._start_scraping, args=(vendor_id, url), daemon=True).start()
                
            except Exception as e:
                print(f"Error adding vendor {url}: {e}")
        
        response = {
            'success': True,
            'vendor_ids': vendor_ids,
            'message': f'Added {len(vendor_ids)} vendors'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_remove_vendor(self, vendor_id):
        try:
            self.db.remove_vendor(vendor_id)
            response = {'success': True, 'message': 'Vendor removed successfully'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_scrape_vendor(self, vendor_id):
        try:
            # Get vendor info
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,))
            vendor = cursor.fetchone()
            conn.close()
            
            if vendor:
                # Start scraping in background
                threading.Thread(target=self._start_scraping, args=(vendor_id, vendor[2]), daemon=True).start()
                response = {'success': True, 'message': 'Scraping started'}
            else:
                response = {'success': False, 'error': 'Vendor not found'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_extract_vendor(self, vendor_id):
        try:
            # Get vendor info
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,))
            vendor = cursor.fetchone()
            conn.close()
            
            if vendor:
                # Start extraction in background
                threading.Thread(target=self._start_extraction, args=(vendor_id,), daemon=True).start()
                response = {'success': True, 'message': 'Extraction started'}
            else:
                response = {'success': False, 'error': 'Vendor not found'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def api_get_progress(self):
        """Get scraping progress for all vendors"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id, status, pages_scraped, total_pages FROM vendors WHERE status = "scraping"')
            scraping_vendors = cursor.fetchall()
            conn.close()
            
            progress = {}
            for vendor in scraping_vendors:
                vendor_id, status, pages_scraped, total_pages = vendor
                progress[vendor_id] = {
                    'status': status,
                    'pages_scraped': pages_scraped or 0,
                    'total_pages': total_pages or 0,
                    'percentage': int((pages_scraped or 0) / (total_pages or 1) * 100) if total_pages else 0
                }
            
            response = {'success': True, 'progress': progress}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _start_scraping(self, vendor_id, url):
        try:
            print(f"Starting scraping for vendor {vendor_id}: {url}")
            self.db.update_vendor_status(vendor_id, 'scraping')
            
            # Define callback to save each page immediately
            def save_page_callback(page_data):
                self._save_single_page(vendor_id, page_data)
            
            # Scrape entire site (excluding blogs) with progress callback
            def progress_callback(pages_scraped, total_pages):
                self.db.update_scraping_progress(vendor_id, pages_scraped, total_pages)
            
            all_content = self.scraper.scrape_entire_site(url, progress_callback=progress_callback, save_callback=save_page_callback)
            
            if all_content:
                self.db.update_vendor_status(vendor_id, 'scraped')
                self.db.update_html_stored(vendor_id, True)
                print(f"Scraping completed for vendor {vendor_id} - {len(all_content)} pages scraped")
            else:
                self.db.update_vendor_status(vendor_id, 'error')
                print(f"Scraping failed for vendor {vendor_id}")
                
        except Exception as e:
            print(f"Error scraping vendor {vendor_id}: {e}")
            self.db.update_vendor_status(vendor_id, 'error')
    
    def _save_single_page(self, vendor_id, page_data):
        """Save a single page immediately after scraping"""
        try:
            url = page_data['url']
            content = page_data['content']
            index = page_data['index']
            
            # Create research_output directory if it doesn't exist
            output_dir = '../research_output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Get vendor name for folder
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM vendors WHERE id = ?', (vendor_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                vendor_name = result[0]
                # Clean vendor name for folder name (same format as original)
                safe_name = re.sub(r'[^\w\-_\.\s]', '', vendor_name)
                safe_name = safe_name.replace(' ', '_')
                vendor_dir = os.path.join(output_dir, safe_name)
                
                if not os.path.exists(vendor_dir):
                    os.makedirs(vendor_dir)
                
                # Create filename from URL (same format as original)
                url_parts = url.replace('https://', '').replace('http://', '').split('/')
                if len(url_parts) > 1:
                    filename = '_'.join(url_parts[1:]) if url_parts[1:] else 'index'
                else:
                    filename = 'index'
                
                # Clean filename
                filename = re.sub(r'[^\w\-_\.]', '_', filename)
                if not filename:
                    filename = f'page_{index}'
                
                # Format content as Markdown
                markdown_content = f"""# {filename.replace('_', ' ').title()}

**URL**: {url}

## Content

{content}
"""
                
                # Save as Markdown file
                md_file = os.path.join(vendor_dir, f'page_{index}_{filename}.md')
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                print(f"Page {index} saved immediately to: {md_file}")
            
        except Exception as e:
            print(f"Error saving single page for vendor {vendor_id}: {e}")
    
    def _save_all_pages_to_files(self, vendor_id, all_content):
        try:
            # Create research_output directory if it doesn't exist
            output_dir = '../research_output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Get vendor name for folder
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM vendors WHERE id = ?', (vendor_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                vendor_name = result[0]
                # Clean vendor name for folder name (same format as original)
                safe_name = re.sub(r'[^\w\-_\.\s]', '', vendor_name)
                safe_name = safe_name.replace(' ', '_')
                vendor_dir = os.path.join(output_dir, safe_name)
                
                if not os.path.exists(vendor_dir):
                    os.makedirs(vendor_dir)
                
                # Save each page as a separate file
                for i, page_content in enumerate(all_content):
                    url = page_content['url']
                    content = page_content['content']
                    
                    # Create filename from URL (same format as original)
                    url_parts = url.replace('https://', '').replace('http://', '').split('/')
                    if len(url_parts) > 1:
                        filename = '_'.join(url_parts[1:]) if url_parts[1:] else 'index'
                    else:
                        filename = 'index'
                    
                    # Clean filename
                    filename = re.sub(r'[^\w\-_\.]', '_', filename)
                    if not filename:
                        filename = f'page_{i+1}'
                    
                    # Format content as Markdown
                    markdown_content = f"""# {filename.replace('_', ' ').title()}

**URL**: {url}

## Content

{content}
"""
                    
                    # Save as Markdown file
                    md_file = os.path.join(vendor_dir, f'page_{i+1}_{filename}.md')
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    print(f"Page {i+1} saved to: {md_file}")
                
                print(f"All {len(all_content)} pages saved for vendor {vendor_id}")
            
        except Exception as e:
            print(f"Error saving pages for vendor {vendor_id}: {e}")
    
    def _save_html_to_file(self, vendor_id, url, html_content):
        try:
            # Create research_output directory if it doesn't exist
            output_dir = '../research_output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Get vendor name for folder
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM vendors WHERE id = ?', (vendor_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                vendor_name = result[0]
                # Clean vendor name for folder name (same format as original)
                safe_name = re.sub(r'[^\w\-_\.\s]', '', vendor_name)
                safe_name = safe_name.replace(' ', '_')
                vendor_dir = os.path.join(output_dir, safe_name)
                
                if not os.path.exists(vendor_dir):
                    os.makedirs(vendor_dir)
                
                # Save HTML file with same naming convention
                html_file = os.path.join(vendor_dir, f'page_{vendor_id}_scraped.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"HTML saved to: {html_file}")
            
        except Exception as e:
            print(f"Error saving HTML for vendor {vendor_id}: {e}")
    
    def _start_extraction(self, vendor_id):
        try:
            print(f"Starting extraction for vendor {vendor_id}")
            self.db.update_vendor_status(vendor_id, 'extracting')
            
            # Get vendor info
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,))
            vendor = cursor.fetchone()
            conn.close()
            
            if vendor:
                # Read HTML from stored file
                html_content = self._read_html_from_file(vendor_id)
                
                if html_content:
                    # Extract services and products
                    services, products = self.extractor.extract_services_products(html_content)
                    
                    # Save to database
                    for service in services:
                        self.db.add_service(vendor_id, service)
                    
                    for product in products:
                        self.db.add_product(vendor_id, product)
                    
                    # Create markdown report in same format as original
                    self._create_markdown_report(vendor_id, vendor, html_content, services, products)
                    
                    self.db.update_vendor_status(vendor_id, 'completed')
                    print(f"Extraction completed for vendor {vendor_id}")
                else:
                    self.db.update_vendor_status(vendor_id, 'error')
                    print(f"Extraction failed for vendor {vendor_id} - no HTML file found")
            
        except Exception as e:
            print(f"Error extracting vendor {vendor_id}: {e}")
            self.db.update_vendor_status(vendor_id, 'error')
    
    def _read_html_from_file(self, vendor_id):
        try:
            # Get vendor name for folder
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM vendors WHERE id = ?', (vendor_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                vendor_name = result[0]
                # Clean vendor name for folder name
                safe_name = re.sub(r'[^\w\-_\.]', '_', vendor_name)
                content_dir = 'scraped_content'
                vendor_dir = os.path.join(content_dir, safe_name)
                html_file = os.path.join(vendor_dir, f'{vendor_id}_scraped.html')
                
                if os.path.exists(html_file):
                    with open(html_file, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    print(f"HTML file not found: {html_file}")
                    return None
            return None
            
        except Exception as e:
            print(f"Error reading HTML file for vendor {vendor_id}: {e}")
            return None
    
    def _create_markdown_report(self, vendor_id, vendor, html_content, services, products):
        try:
            # Create research_output directory if it doesn't exist
            output_dir = '../research_output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            vendor_name = vendor[1]
            website = vendor[2]
            
            # Clean vendor name for folder name (same format as original)
            safe_name = re.sub(r'[^\w\-_\.\s]', '', vendor_name)
            safe_name = safe_name.replace(' ', '_')
            vendor_dir = os.path.join(output_dir, safe_name)
            
            if not os.path.exists(vendor_dir):
                os.makedirs(vendor_dir)
            
            # Create markdown report in same format as original
            markdown_content = f"""# {vendor_name}

**URL**: {website}

## Content

{html_content[:5000]}...

## Services Mentioned
{', '.join(services[:10]) if services else 'No services found'}

## Technology Stack
{', '.join(products[:10]) if products else 'No products found'}

## Contact Information
{{
  "website": "{website}",
  "vendor_id": {vendor_id}
}}
"""
            
            # Save markdown file
            markdown_file = os.path.join(vendor_dir, f'page_{vendor_id}_extracted.md')
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Markdown report saved to: {markdown_file}")
            
        except Exception as e:
            print(f"Error creating markdown report for vendor {vendor_id}: {e}")

def main():
    PORT = 61541
    
    # Check if trafilatura is available
    try:
        import trafilatura
        print(f"✅ Trafilatura available: {trafilatura.__version__}")
    except ImportError:
        print("⚠️  Trafilatura not available, using fallback extraction")
    
    print(f"🎭 Using Playwright for undetectable scraping")
    print(f"Starting Complete Vendor Research Server on port {PORT}")
    print(f"Access the application at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleWebHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use. Please stop the existing server first.")
            print("You can stop it with: pkill -f complete_server.py")
        else:
            print(f"Error starting server: {e}")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
