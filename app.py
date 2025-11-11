from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Add this import
import random
import string
import re
import os

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)  # Add this line to enable CORS

class PasswordManager:
    # ... rest of your existing PasswordManager class ...

manager = PasswordManager()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        length = int(data.get('length', 16))
        if length < 8 or length > 50:
            return jsonify({'error': 'Password length must be between 8 and 50'}), 400
            
        password = manager.generate_password(length)
        strength = manager.check_strength(password)
        return jsonify({'password': password, 'strength': strength})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/check', methods=['POST'])
def check():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        password = data.get('password', '')
        if not password:
            return jsonify({'error': 'No password provided'}), 400
            
        strength = manager.check_strength(password)
        return jsonify({'strength': strength})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Add this route to serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("🔐 GenCheckPass starting...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
