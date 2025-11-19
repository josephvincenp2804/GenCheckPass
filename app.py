from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import string
import re
import os

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

class PasswordManager:

    def generate_password(self, length=16):
        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}"
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def check_strength(self, password):
        score = 0
        feedback = []

        length = len(password)
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        else:
            feedback.append("Increase password length")

        if re.search(r"[A-Z]", password): score += 15
        else: feedback.append("Add uppercase letters")

        if re.search(r"[a-z]", password): score += 15
        else: feedback.append("Add lowercase letters")

        if re.search(r"[0-9]", password): score += 20
        else: feedback.append("Include numbers")

        if re.search(r"[!@#$%^&*()\-_=+\[\]{}]", password): score += 25
        else: feedback.append("Use special characters")

        if score >= 90:
            strength = "Very Strong"
        elif score >= 70:
            strength = "Strong"
        elif score >= 50:
            strength = "Good"
        elif score >= 30:
            strength = "Weak"
        else:
            strength = "Very Weak"

        return {
            "score": score,
            "max_score": 100,
            "strength": strength,
            "feedback": feedback
        }

manager = PasswordManager()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    length = int(data.get('length', 16))
    password = manager.generate_password(length)
    strength = manager.check_strength(password)
    return jsonify({'password': password, 'strength': strength})

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get('password', '')
    strength = manager.check_strength(password)
    return jsonify({'strength': strength})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("🔐 GenCheckPass running on localhost")
    app.run(host='0.0.0.0', port=5000)
