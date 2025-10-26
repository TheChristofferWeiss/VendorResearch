"""
Background startup script for the Vendor Research Web Application.
"""

import os
import sys
import subprocess
import time

def main():
    """Start the web application in background."""
    print("Starting Vendor Research Web Application in background...")
    
    # Check if we're in the right directory
    if not os.path.exists('web_app/simple_web_server.py'):
        print("Error: web_app/simple_web_server.py not found")
        print("Please run this script from the VendorResearch directory")
        return
    
    try:
        # Start the web server in background
        os.chdir('web_app')
        
        # Start the server process
        process = subprocess.Popen([sys.executable, 'simple_web_server.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Give the server time to start and find a port
        time.sleep(3)
        
        if process.poll() is None:
            print("✓ Server started successfully in background")
            print("✓ Server is running and accessible via web browser")
            print("✓ Check the terminal output above for the server URL")
            print("\nTo stop the server, run: pkill -f simple_web_server.py")
        else:
            print("✗ Failed to start server")
            stderr = process.stderr.read()
            if stderr:
                print(f"Error: {stderr}")
                
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
