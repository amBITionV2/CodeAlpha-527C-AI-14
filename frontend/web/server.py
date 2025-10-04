#!/usr/bin/env python3
"""
SignSpeak AI - Web Frontend Server
Simple HTTP server to serve the web frontend
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_web_server(port=3000):
    """Start the web server"""
    # Change to the web directory
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    # Create server
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print(f"SignSpeak AI Web Frontend")
        print(f"Server running on http://localhost:{port}")
        print(f"Open your browser and navigate to the URL above")
        print(f"Make sure the backend is running on http://localhost:5000")
        print(f"Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{port}')
            print("Browser opened automatically")
        except:
            print("Please open your browser manually")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            sys.exit(0)

if __name__ == "__main__":
    port = 3000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number, using default port 3000")
    
    start_web_server(port)
