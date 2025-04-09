from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import time
from collections import deque
from typing import Dict, List, Any

app = Flask(__name__)
CORS(app)  # Allows CORS for all domens

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# storage for all the packets
packages = deque(maxlen=5000)
lock = threading.Lock()
transmission_active = False 

@app.route('/api/packages', methods=['POST'])
def receive_package():
    """Endpoint for packets recieving"""
    data = request.get_json()

    if data.get('is_last'):
        with lock:
            global transmission_active
            transmission_active = False
        return jsonify({'status': 'transmission_complete'}), 200
    
    if not transmission_active:
        with lock:
            packages.clear()  # Clear previous data
            transmission_active = True
    
    if not data or not all(key in data for key in ['ip', 'latitude', 'longitude', 'timestamp', 'suspicious']):
        return jsonify({'error': 'Invalid package format'}), 400
    
    with lock:
        packages.append(data)
    
    return jsonify({'status': 'success'}), 200

@app.route('/api/packages', methods=['GET'])
def get_packages():
    """Endpoint for packets recieving (for frontend)"""
    with lock:
        return jsonify(list(packages))

def start_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    start_server()