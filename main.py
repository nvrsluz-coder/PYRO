from flask import Flask, request, Response
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Asl server URL (sizning pyro serveringiz)
REAL_SERVER_URL = "https://pyro-7d2f.onrender.com"

@app.route('/run-pastebin')
def run_pastebin():
    """Foydalanuvchi uchun asosiy endpoint"""
    try:
        # Asl serverga so'rov yuborish
        response = requests.get(
            f"{REAL_SERVER_URL}/run",
            timeout=30
        )
        
        # Xuddi shu status code va headerni qaytarish
        return Response(
            response.text,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'text/plain')
        )
    except requests.exceptions.Timeout:
        return "Server timeout", 504
    except requests.exceptions.ConnectionError:
        return "Connection error", 502
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/health')
def health():
    """Sog'likni tekshirish uchun"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": REAL_SERVER_URL
    }

@app.route('/')
def home():
    """Bosh sahifa"""
    return """
    <h1>Pastebin Gateway Server</h1>
    <p>Foydalanish uchun: /run-pastebin endpointiga so'rov yuboring</p>
    <p>Example: <a href='/run-pastebin'>/run-pastebin</a></p>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
