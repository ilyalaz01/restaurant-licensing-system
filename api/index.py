"""
Step-by-step diagnostic to find what's breaking
"""
from http.server import BaseHTTPRequestHandler
import json

# Uncomment these ONE AT A TIME to find what breaks:

# Step 1: Test if FastAPI import works
# from fastapi import FastAPI

# Step 2: Test if your services import works  
# from services import gemini_service

# Step 3: Test if Firebase import works
# import firebase_admin

class handler(BaseHTTPRequestHandler):
    def _send_json(self, data: dict, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        response = {
            "status": "working",
            "message": "Step 1: Base handler works",
        }
        self._send_json(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()