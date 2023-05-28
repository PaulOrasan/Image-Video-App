from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
CORS(app)
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Perform validation against your authentication system
    if username == 'a' and password == 'a':
        # Valid credentials
        access_token = create_access_token(identity=username, expires_delta=False)
        return make_response(jsonify({'access_token': access_token})), 200
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/', methods=['GET'])
@jwt_required()
def main_page():
    current_user = get_jwt_identity()
    print(current_user)
    return make_response(f"Hey {current_user}"), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
