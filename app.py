from flask import Flask, request, jsonify, send_file
import random
import string
import re

app = Flask(__name__)

class PasswordManager:
    def __init__(self):
        pass
    
    def generate_password(self, length=16):
        """Generate strong random password with all character types"""
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digits = random.choice(string.digits)
        symbols = random.choice("!@#$%&*")
        
        remaining_length = length - 4
        all_chars = string.ascii_letters + string.digits + "!@#$%&*"
        remaining = ''.join(random.choice(all_chars) for _ in range(remaining_length))
        
        password = uppercase + lowercase + digits + symbols + remaining
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)
    
    def check_strength(self, password):
        """Enhanced password strength check"""
        score = 0
        feedback = []
        
        # Length (max 30 points)
        if len(password) >= 8: score += 10
        if len(password) >= 12: score += 10
        if len(password) >= 16: score += 10
        
        # Character types (max 40 points)
        if re.search(r'[A-Z]', password): score += 10
        else: feedback.append("Add uppercase letters")
            
        if re.search(r'[a-z]', password): score += 10
        else: feedback.append("Add lowercase letters")
            
        if re.search(r'\d', password): score += 10
        else: feedback.append("Add numbers")
            
        if re.search(r'[!@#$%&*]', password): score += 10
        else: feedback.append("Add symbols")
        
        # Complexity bonus (max 30 points)
        char_types = sum([
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'[!@#$%&*]', password))
        ])
        
        if char_types == 4: score += 30
        elif char_types == 3: score += 15
        elif char_types == 2: score += 5
        
        # Final rating
        if score >= 80:
            strength = "Very Strong 💪"
        elif score >= 60:
            strength = "Strong 👍"
        elif score >= 40:
            strength = "Good ✅"
        elif score >= 20:
            strength = "Weak ⚠️"
        else:
            strength = "Very Weak ❌"
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'max_score': 100
        }

manager = PasswordManager()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    length = int(request.json.get('length', 16))
    password = manager.generate_password(length)
    strength = manager.check_strength(password)
    
    return jsonify({
        'password': password,
        'strength': strength
    })

@app.route('/check', methods=['POST'])
def check():
    password = request.json.get('password', '')
    strength = manager.check_strength(password)
    
    return jsonify({'strength': strength})

if __name__ == '__main__':
    print("🔐 GenCheckPass starting...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)