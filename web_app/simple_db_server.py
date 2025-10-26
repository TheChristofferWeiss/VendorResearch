#!/usr/bin/env python3
"""
Simple Database Server
"""

import http.server
import socketserver
import json
import sqlite3
import socket
from urllib.parse import urlparse

class SimpleWebHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(f"GET request for: {self.path}")
        
        if self.path == '/':
            self.serve_dashboard()
        elif self.path == '/admin':
            self.serve_admin()
        else:
            self.send_error(404)
    
    def do_POST(self):
        print(f"POST request for: {self.path}")
        
        if self.path == '/api/vendors':
            self.api_add_vendor()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        # Get vendors from database
        conn = sqlite3.connect('vendor_research.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors ORDER BY created_at DESC')
        vendors = cursor.fetchall()
        conn.close()
        
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
        # Get vendors from database
        conn = sqlite3.connect('vendor_research.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vendors ORDER BY created_at DESC')
        vendors = cursor.fetchall()
        conn.close()
        
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
            </div>
            """
        return html
    
    def _render_vendor_table(self, vendors):
        if not vendors:
            return "<tr><td colspan='4'>No vendors found.</td></tr>"
        
        html = ""
        for vendor in vendors:
            html += f"""
            <tr>
                <td>{vendor[0]}</td>
                <td>{vendor[1]}</td>
                <td><a href="{vendor[2]}" target="_blank">{vendor[2]}</a></td>
                <td>{vendor[4]}</td>
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
        
        # Add vendors to database
        conn = sqlite3.connect('vendor_research.db')
        cursor = conn.cursor()
        
        for url in url_list:
            try:
                domain = urlparse(url).netloc
                cursor.execute('''
                    INSERT INTO vendors (name, website, description)
                    VALUES (?, ?, ?)
                ''', (domain, url, f"Vendor from {domain}"))
                vendor_ids.append(cursor.lastrowid)
            except Exception as e:
                print(f"Error adding vendor {url}: {e}")
        
        conn.commit()
        conn.close()
        
        response = {
            'success': True,
            'vendor_ids': vendor_ids,
            'message': f'Added {len(vendor_ids)} vendors'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    PORT = find_free_port()
    
    print(f"Starting Simple Database Server on port {PORT}")
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
