#!/usr/bin/env python3
"""
Working Vendor Research Web Server
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
        
        conn.commit()
        conn.close()
    
    def add_vendor(self, name, website, description=""):
        """Add a new vendor."""
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
        """Get all vendors."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM vendors ORDER BY created_at DESC')
        vendors = cursor.fetchall()
        
        conn.close()
        return vendors
    
    def remove_vendor(self, vendor_id):
        """Remove a vendor."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0

class SimpleWebHandler(http.server.BaseHTTPRequestHandler):
    """Simple web handler for the vendor research system."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = SimpleVendorDB()
    
    def do_GET(self):
        """Handle GET requests."""
        print(f"GET request for: {self.path}")
        
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/admin':
            self.serve_admin()
        elif self.path == '/chat':
            self.serve_chat()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        print(f"POST request for: {self.path}")
        
        if self.path == '/api/vendors':
            self.api_add_vendor()
        elif self.path.startswith('/api/vendors/') and self.path.endswith('/remove'):
            vendor_id = int(self.path.split('/')[-2])
            self.api_remove_vendor(vendor_id)
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
                .btn {{ 
                    padding: 8px 16px; 
                    margin: 5px; 
                    text-decoration: none; 
                    border-radius: 3px; 
                    cursor: pointer; 
                    border: none;
                }}
                .btn-primary {{ background: #007bff; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Vendor Research Dashboard</h1>
                <p>Manage and research vendors</p>
                <a href="/admin" class="btn btn-primary">Admin Panel</a>
                <a href="/chat" class="btn btn-primary">Chat Interface</a>
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
                
                function removeVendor(id) {{
                    if (confirm('Are you sure you want to remove this vendor?')) {{
                        fetch(`/api/vendors/${{id}}/remove`, {{ method: 'POST' }})
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
            </style>
        </head>
        <body>
            <h1>Chat Interface</h1>
            <p>Chat functionality will be implemented here.</p>
            <a href="/">Back to Dashboard</a>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _render_vendors(self, vendors):
        """Render vendors for the dashboard."""
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
            </div>
            """
        return html
    
    def _render_vendor_table(self, vendors):
        """Render vendors for the admin table."""
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
                    <button class="btn btn-danger" onclick="removeVendor({vendor[0]})">Remove</button>
                </td>
            </tr>
            """
        return html
    
    def api_add_vendor(self):
        """API endpoint to add vendors."""
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
        
        # Parse URLs
        url_list = [url.strip() for url in urls.split('\n') if url.strip()]
        vendor_ids = []
        
        for url in url_list:
            try:
                # Extract domain name for vendor name
                domain = urlparse(url).netloc
                vendor_id = self.db.add_vendor(domain, url, f"Vendor from {domain}")
                vendor_ids.append(vendor_id)
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

def find_free_port():
    """Find a free port to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Main function to start the web server."""
    PORT = find_free_port()
    
    print(f"Starting Vendor Research Web Server on port {PORT}")
    print(f"Access the application at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    print(f"Chat Interface: http://localhost:{PORT}/chat")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleWebHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
