import waitress
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
# allow cors for http://localhost:5000 and https://0xleft.github.io
CORS(app, resources={r"/*": {"origins": ["http://localhost:8000", "https://0xleft.github.io"]}})
app.config['CORS_HEADERS'] = 'Content-Type'

users = []

@app.route('/api/clear_users', methods=['GET'])
def clear_users():
    users.clear()
    return jsonify({'success': True}), 200

@app.route('/api/get_user_text', methods=['POST'])
def get_user_text():
    data = request.get_json(silent=True, force=True)
    if data is None:
        return jsonify({'success': False, "message": "no data"}), 400

    b = "​"
    c = "‌"

    text = data["text"]
    username = data["username"]

    if len(text) < 30:
        return jsonify({'success': False, "message": "text is too short"}), 400

    # check if username is already taken
    if any(user["username"] == username for user in users):
        return jsonify({'success': False, "message": "username is already used up"}), 400
    
    users.append({
        "username": username,
        "userid": len(users),
    })
    
    binary_id = get_binary(len(users) - 1)

    binary_id = binary_id.replace("0", b)
    binary_id = binary_id.replace("1", c)

    # insert binary_id into text at index 16 (it could be any other index)
    text = text[:16] + binary_id + text[16:]

    return jsonify({'success': True, 'text': text}), 200

# extract binary_id from text at index 16
@app.route('/api/get_user_id', methods=['GET'])
def get_user_id():
    text = request.args.get('text')

    b = "​"
    c = "‌"

    # replace all characters except for b and c
    for char in text:
        if char != b and char != c:
            text = text.replace(char, "")

    binary_id = text

    binary_id = binary_id.replace(b, "0")
    binary_id = binary_id.replace(c, "1")

    user_id = get_int(binary_id)
    
    possible_users = [user["username"] for user in users if user["userid"] == user_id]

    if len(possible_users) == 0:
        return jsonify({'success': False, "message": "id doesn't represent a user"}), 418
    
    username = possible_users[0]

    return jsonify({'success': True, 'username': username}), 200

def get_binary(number: int) -> str:
    return bin(number)[2:]

def get_int(binary: str) -> int:
    return int(binary, 2)

if __name__ == '__main__':
    waitress.serve(app, port=5000)