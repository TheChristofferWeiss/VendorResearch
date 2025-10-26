#!/usr/bin/env python3
"""
Minimal Working Vendor Research Server
"""

import http.server
import socketserver
import json
import socket

class MinimalWebHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
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
        print(f"POST request for: {self.path}")
        
        if self.path == '/api/vendors':
            self.api_add_vendor()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vendor Research Dashboard</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }
                .header { 
                    background: #2d2d2d; 
                    padding: 20px; 
                    border-radius: 5px; 
                    border: 1px solid #444;
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
            <div class="header">
                <h1>Vendor Research Dashboard</h1>
                <p>Manage and research vendors</p>
                <a href="/admin" class="btn btn-primary">Admin Panel</a>
                <a href="/chat" class="btn btn-primary">Chat Interface</a>
            </div>
            
            <h2>Welcome to Vendor Research</h2>
            <p>This is a working server!</p>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_admin(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background-color: #1a1a1a; 
                    color: #e0e0e0; 
                }
                .form-group { margin: 15px 0; }
                label { display: block; margin-bottom: 5px; color: #e0e0e0; }
                input, textarea { 
                    width: 100%; 
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
            <h1>Admin Panel</h1>
            
            <h2>Add Vendor</h2>
            <form id="addVendorForm">
                <div class="form-group">
                    <label for="urls">Vendor URLs (one per line):</label>
                    <textarea id="urls" name="urls" rows="5" placeholder="https://example.com"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Add Vendors</button>
            </form>
            
            <script>
                document.getElementById('addVendorForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const urls = document.getElementById('urls').value;
                    if (!urls.trim()) {
                        alert('Please enter at least one URL');
                        return;
                    }
                    
                    fetch('/api/vendors', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ urls: urls })
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            alert('Vendors added successfully!');
                        } else {
                            alert('Error: ' + result.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error adding vendors: ' + error.message);
                    });
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_chat(self):
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
        
        response = {
            'success': True,
            'message': f'Would add {len(urls.split())} vendors'
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
    
    print(f"Starting Minimal Vendor Research Server on port {PORT}")
    print(f"Access the application at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    print(f"Chat Interface: http://localhost:{PORT}/chat")
    
    try:
        with socketserver.TCPServer(("", PORT), MinimalWebHandler) as httpd:
            print(f"Server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
