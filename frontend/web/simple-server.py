#!/usr/bin/env python3
"""
SignSpeak AI - Simple Working Server
Serves the working interface without complex dependencies
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import time
from pathlib import Path

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Simple HTTP request handler with CORS support"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def start_simple_server(port=3000):
    """Start the simple web server"""
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    try:
        with socketserver.TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("SignSpeak AI - Simple Working Server")
            print("=" * 60)
            print(f"Server running on http://localhost:{port}")
            print(f"Working interface: http://localhost:{port}/simple-production.html")
            print(f"Make sure the backend is running on http://localhost:5000")
            print("=" * 60)
            print("Features:")
            print("✓ Real-time gesture recognition")
            print("✓ Text-to-gesture conversion")
            print("✓ Simple avatar animation")
            print("✓ Working interface without complex dependencies")
            print("=" * 60)
            print("Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open browser automatically
            def open_browser():
                time.sleep(2)  # Wait for server to start
                try:
                    webbrowser.open(f'http://localhost:{port}/simple-production.html')
                    print("Browser opened automatically")
                except Exception as e:
                    print(f"Could not open browser automatically: {e}")
                    print("Please open your browser manually and navigate to the URL above")
            
            # Start browser opening in a separate thread
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Start the server
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Error: Port {port} is already in use")
            print("Please try a different port or stop the process using this port")
            return False
        else:
            print(f"Error starting server: {e}")
            return False
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return True
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    port = 3000
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number, using default port 3000")
    
    print("SignSpeak AI - Simple Working Server")
    print("Starting server...")
    
    # Start the server
    success = start_simple_server(port)
    
    if not success:
        sys.exit(1)
