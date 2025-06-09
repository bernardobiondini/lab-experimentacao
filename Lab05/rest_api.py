
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Carregar dados do arquivo JSON
with open('data.json', 'r') as f:
    users_data = json.load(f)

@app.route('/users', methods=['GET'])
def get_users():
    city = request.args.get('city')
    if city:
        filtered_users = [user for user in users_data if user['city'] == city]
        return jsonify(filtered_users)
    return jsonify(users_data)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users_data if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)


