"""
Startup script for the Vendor Research Web Application.
"""

import os
import sys
import subprocess
import time
import signal
import threading

def main():
    """Start the web application in background."""
    print("Vendor Research Web Application")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('web_app/simple_web_server.py'):
        print("Error: web_app/simple_web_server.py not found")
        print("Please run this script from the VendorResearch directory")
        return
    
    print("Starting the web server in background...")
    print("The server will automatically find an available port.")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Start the web server in background
        os.chdir('web_app')
        
        # Start the server process
        process = subprocess.Popen([sys.executable, 'simple_web_server.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Read output in a separate thread
        def read_output():
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
        
        # Start output reading thread
        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()
        
        # Wait for the process to start
        time.sleep(2)
        
        if process.poll() is None:
            print("✓ Server started successfully in background")
            print("✓ Server is running and accessible via web browser")
            print("\nTo stop the server, press Ctrl+C")
            
            # Wait for user interrupt
            try:
                while process.poll() is None:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping server...")
                process.terminate()
                process.wait()
                print("Server stopped.")
        else:
            print("✗ Failed to start server")
            stderr = process.stderr.read()
            if stderr:
                print(f"Error: {stderr}")
                
    except KeyboardInterrupt:
        print("\nServer startup cancelled.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
