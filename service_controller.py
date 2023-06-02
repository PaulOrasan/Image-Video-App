import datetime
import socket

from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from cryptography.fernet import Fernet

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from repository_persistence import UserRepository
from security_service import SecurityService
from user_service import UserService
from comm_utils import OK, UNAUTHORIZED, REFUSED, BAD_REQUEST

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key
CORS(app)
jwt = JWTManager(app)
user_service = UserService(UserRepository())
security_service = SecurityService()

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the request
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return make_response(), BAD_REQUEST
    # Perform validation against your authentication system
    if user_service.check_user_credentials(email, password):
        # Valid credentials
        is_admin = email == 'admin'
        access_token = create_access_token(identity=email, expires_delta=None)
        return make_response(jsonify({'access_token': access_token, 'admin': is_admin})), OK
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid credentials'}), UNAUTHORIZED

@app.route('/', methods=['GET'])
@jwt_required()
def main_page():
    current_user = get_jwt_identity()
    print(current_user)
    return make_response(f"Hey {current_user}"), OK

@app.route('/data', methods=['GET'])
@jwt_required()
def get_history_of_user():
    images = [
        'fire.103.png',
        'fire.110.png',
        'fire.122.png'
    ]
    email = get_jwt_identity()
    user = user_service.find_user_by_email(email)
    if not user.is_authorized:
        return make_response(), REFUSED
    return make_response(jsonify({"images": [security_service.encrypt_resource(img) for img in images]})), OK

@app.route('/images/<name>')
def get_image(name):
    # Set the directory path where the images are stored
    print(name)
    image_directory = 'images'
    name = security_service.decrypt_resource(name)
    # Serve the image file from the specified directory
    return send_from_directory(image_directory, name.decode())


@app.route('/signup', methods=['POST'])
def add_new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return make_response(), BAD_REQUEST
    user = user_service.register_new_user(email, password)
    if user is None:
        return make_response(), REFUSED
    return make_response(), OK


@app.route('/admin', methods=['GET'])
@jwt_required()
def get_admin_data():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user != 'admin':
        return make_response('naughty naughty'), UNAUTHORIZED
    return make_response(jsonify({'data':[{'email': u.email, 'authorization': u.is_authorized,
                                   'registration_time': u.registration_time} for u in user_service.find_all_users()]})), OK

@app.route('/admin/authorizations', methods=['PUT'])
# @jwt_required()
def get_update_authorization():
    # email = get_jwt_identity()
    username = request.json.get('email')
    flag = request.json.get('authorization')
    # print(email, username, flag)
    user_service.update_authorization(username, flag)
    return make_response(), OK

if __name__ == '__main__':
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('localhost', 8000))
    # sock.listen(1)
    # print('Service B is listening...')
    app.run(debug=True, port=5000)
