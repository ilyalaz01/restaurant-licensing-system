"""
Super minimal working Python API for Vercel
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        path = self.path

        if path in ["/", "/api", "/api/"]:
            response = {
                "status": "working",
                "message": "Minimal Python API running on Vercel!",
                "timestamp": datetime.now().isoformat(),
                "path": path,
            }
        elif path == "/api/health":
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            response = {"error": "Not found", "path": path}

        self._send_json(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        self._send_json({"message": "POST working", "path": self.path})
