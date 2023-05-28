from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from cryptography.fernet import Fernet

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
CORS(app)
jwt = JWTManager(app)
fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)

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


def encrypt_filename(cyp, filename):
    return cyp.encrypt(filename.encode()).decode()
@app.route('/history', methods=['GET'])
@jwt_required()
def get_history_of_user():
    images = [
        'fire.103.png',
        'fire.110.png',
        'fire.122.png'
    ]
    return make_response(jsonify({"images": [encrypt_filename(cipher, img) for img in images]}))


@app.route('/images/<name>')
def get_image(name):
    # Set the directory path where the images are stored
    image_directory = 'images'
    name = cipher.decrypt(name.encode())
    # Serve the image file from the specified directory
    return send_from_directory(image_directory, name.decode())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
