#!/usr/bin/env python3
"""
SignSpeak AI - Production Web Server
Serves the production frontend with proper CORS and static file handling
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time
from pathlib import Path

class ProductionHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support"""
    
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

def start_production_server(port=3000):
    """Start the production web server"""
    web_dir = Path(__file__).parent
    os.chdir(web_dir)
    
    # Check if required files exist
    required_files = ['production.html', 'production-styles.css', 'production-script.js', 'three_js_avatar.js']
    missing_files = [f for f in required_files if not (web_dir / f).exists()]
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        return False
    
    try:
        with socketserver.TCPServer(("", port), ProductionHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("SignSpeak AI - Production Web Server")
            print("=" * 60)
            print(f"Server running on http://localhost:{port}")
            print(f"Production interface: http://localhost:{port}/production.html")
            print(f"Make sure the backend is running on http://localhost:5000")
            print("=" * 60)
            print("Features:")
            print("✓ Real-time gesture recognition")
            print("✓ Speech processing (multiple languages)")
            print("✓ 3D avatar animation with Three.js")
            print("✓ Text-to-gesture conversion")
            print("✓ Production-ready interface")
            print("=" * 60)
            print("Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open browser automatically
            def open_browser():
                time.sleep(2)  # Wait for server to start
                try:
                    webbrowser.open(f'http://localhost:{port}/production.html')
                    print("Browser opened automatically")
                except Exception as e:
                    print(f"Could not open browser automatically: {e}")
                    print("Please open your browser manually and navigate to the URL above")
            
            # Start browser opening in a separate thread
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

def check_backend_connection():
    """Check if the backend API is running"""
    try:
        import requests
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("Backend API Status: [OK] Connected")
            print(f"Systems: Gesture Recognition={data.get('systems', {}).get('gesture_recognition', False)}, Speech Processing={data.get('systems', {}).get('speech_processing', False)}")
            return True
        else:
            print("Backend API Status: [ERROR] Not responding properly")
            return False
    except Exception as e:
        print("Backend API Status: [ERROR] Not reachable")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    port = 3000
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number, using default port 3000")
    
    print("SignSpeak AI - Production Web Server")
    print("Checking system requirements...")
    
    # Check backend connection
    backend_available = check_backend_connection()
    
    if not backend_available:
        print("\nWarning: Backend API is not available!")
        print("Please start the backend server first:")
        print("  python backend/app_production.py")
        print("\nThe frontend will still work but with limited functionality.")
        print("=" * 60)
    
    # Start the server
    success = start_production_server(port)
    
    if not success:
        sys.exit(1)
