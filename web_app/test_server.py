#!/usr/bin/env python3
"""
Test server to debug the 404 issue.
"""

import http.server
import socketserver
import socket

def find_free_port():
    """Find a free port to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

class TestHandler(http.server.BaseHTTPRequestHandler):
    """Test handler to debug the 404 issue."""
    
    def do_GET(self):
        """Handle GET requests."""
        print(f"Received GET request for: {self.path}")
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Test Server Working!</h1><p>Server is responding correctly.</p>')
        elif self.path == '/admin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Admin Panel</h1><p>Admin panel is working!</p>')
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        print(f"Received POST request for: {self.path}")
        
        if self.path == '/api/vendors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"success": true, "message": "Test API working"}')
        else:
            self.send_error(404)

def main():
    """Main function to start the test server."""
    PORT = find_free_port()
    
    print(f"Starting Test Server on port {PORT}")
    print(f"Access the test server at: http://localhost:{PORT}")
    print(f"Admin Panel: http://localhost:{PORT}/admin")
    
    try:
        with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
            print(f"Test server running on http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting test server: {e}")

if __name__ == "__main__":
    main()
