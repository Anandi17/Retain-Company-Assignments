from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def home():
    return "User Management System", 200

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    users_list = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
    return jsonify(users_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({"id": user[0], "name": user[1], "email": user[2]}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (name, email, hashed_password))
    conn.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                   (name, email, user_id))
    conn.commit()
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return jsonify({"message": f"User {user_id} deleted"}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
    users = cursor.fetchall()
    users_list = [{"id": u[0], "name": u[1], "email": u[2]} for u in users]
    return jsonify(users_list), 200

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid credentials"}), 400

    cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        return jsonify({"status": "success", "user_id": user[0]}), 200
    return jsonify({"status": "failed"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
