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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
        cursor.execute('SELECT * FROM vendors ORDER BY created_at DESC')
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

class SimpleScraper:
    def __init__(self):
        self.session = None
    
    def scrape_url(self, url):
        try:
            # Use curl to bypass SSL issues
            cmd = ['curl', '-s', '-L', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Curl error for {url}: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

class SimpleExtractor:
    def __init__(self):
        pass
    
    def extract_services_products(self, html_content):
        if not html_content:
            return [], []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            # Simple extraction based on common patterns
            services = []
            products = []
            
            # Look for service-related keywords
            service_keywords = ['service', 'solution', 'platform', 'software', 'tool', 'system']
            product_keywords = ['product', 'software', 'app', 'tool', 'platform', 'solution']
            
            # Extract text blocks that might contain services/products
            paragraphs = soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            for p in paragraphs:
                text = p.get_text().strip().lower()
                if any(keyword in text for keyword in service_keywords):
                    if len(text) > 10 and len(text) < 200:
                        services.append(text)
                if any(keyword in text for keyword in product_keywords):
                    if len(text) > 10 and len(text) < 200:
                        products.append(text)
            
            # Remove duplicates and limit results
            services = list(set(services))[:10]
            products = list(set(products))[:10]
            
            return services, products
            
        except Exception as e:
            print(f"Error extracting content: {e}")
            return [], []

class SimpleWebHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = SimpleVendorDB()
        self.scraper = SimpleScraper()
        self.extractor = SimpleExtractor()
        self.scraping_progress = {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(f"GET request for: {self.path}")
        
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/admin':
            self.serve_admin()
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
            <table class="vendor-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Website</th>
                        <th>Status</th>
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
                            alert('Vendors added successfully!');
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
                                alert('Vendor removed successfully!');
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
            return "<tr><td colspan='5'>No vendors found.</td></tr>"
        
        html = ""
        for vendor in vendors:
            html += f"""
            <tr>
                <td>{vendor[0]}</td>
                <td>{vendor[1]}</td>
                <td><a href="{vendor[2]}" target="_blank">{vendor[2]}</a></td>
                <td>{vendor[4]}</td>
                <td>
                    <button class="btn btn-success" onclick="scrapeVendor({vendor[0]})">Scrape</button>
                    <button class="btn btn-warning" onclick="extractVendor({vendor[0]})">Extract</button>
                    <button class="btn btn-danger" onclick="removeVendor({vendor[0]})">Remove</button>
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
    
    def _start_scraping(self, vendor_id, url):
        try:
            print(f"Starting scraping for vendor {vendor_id}: {url}")
            self.db.update_vendor_status(vendor_id, 'scraping')
            
            # Scrape the URL
            html_content = self.scraper.scrape_url(url)
            
            if html_content:
                self.db.update_vendor_status(vendor_id, 'scraped')
                print(f"Scraping completed for vendor {vendor_id}")
            else:
                self.db.update_vendor_status(vendor_id, 'error')
                print(f"Scraping failed for vendor {vendor_id}")
                
        except Exception as e:
            print(f"Error scraping vendor {vendor_id}: {e}")
            self.db.update_vendor_status(vendor_id, 'error')
    
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
                # Scrape content first
                html_content = self.scraper.scrape_url(vendor[2])
                
                if html_content:
                    # Extract services and products
                    services, products = self.extractor.extract_services_products(html_content)
                    
                    # Save to database
                    for service in services:
                        self.db.add_service(vendor_id, service)
                    
                    for product in products:
                        self.db.add_product(vendor_id, product)
                    
                    self.db.update_vendor_status(vendor_id, 'completed')
                    print(f"Extraction completed for vendor {vendor_id}")
                else:
                    self.db.update_vendor_status(vendor_id, 'error')
                    print(f"Extraction failed for vendor {vendor_id}")
            
        except Exception as e:
            print(f"Error extracting vendor {vendor_id}: {e}")
            self.db.update_vendor_status(vendor_id, 'error')

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    PORT = find_free_port()
    
    print(f"Starting Complete Vendor Research Server on port {PORT}")
    print(f"Access the application at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleWebHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
