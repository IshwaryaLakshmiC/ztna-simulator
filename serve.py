#!/usr/bin/env python3
"""
Local dev server for the Identity & Access Decision Studio.
Serves index.html for ALL routes so Okta redirect callback works.

Usage: python3 serve.py
"""
import http.server
import os

PORT = 8080
DIR  = os.path.dirname(os.path.abspath(__file__))

class SPAHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html for every request regardless of path
        # This is what makes http://localhost:8080/ work after Okta redirect
        filepath = os.path.join(DIR, 'index.html')
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'index.html not found')

    def log_message(self, fmt, *args):
        # Suppress per-request logs for cleaner output
        pass

if __name__ == '__main__':
    server = http.server.HTTPServer(('', PORT), SPAHandler)
    print(f'\n  Identity & Access Decision Studio running at http://localhost:{PORT}/')
    print(f'  Okta redirect URI to whitelist: http://localhost:{PORT}/')
    print('\n  Ctrl+C to stop\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
