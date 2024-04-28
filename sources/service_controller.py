import datetime
import logging
import socket
import time
from io import BytesIO

from PIL import Image
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from cryptography.fernet import Fernet
from gradio_client import Client
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from media_service import MediaService
from predictions_service import PredictionService
from repository_persistence import UserRepository, MediaResourceRepository, PredictionRepository
from security_service import SecurityService
from user_service import UserService
from comm_utils import OK, UNAUTHORIZED, REFUSED, BAD_REQUEST

app = Flask(__name__)
app.config.from_file('config.json', load=True)
CORS(app)
jwt = JWTManager(app)
user_service = UserService(UserRepository())
media_service = MediaService(MediaResourceRepository())
predictions_service = PredictionService(PredictionRepository())
security_service = SecurityService()
model_client = Client(app.config['GRADIO_MODEL_SERVICE'])

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
@app.before_request
@app.after_request
def log_request():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    logging.info(f'{current_time}: Request: {request.method} {request.path}')

@app.errorhandler(Exception)
def log_error(error):
    logging.error(f'Error: {error}')
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
        is_admin = email == app.config['ADMIN_EMAIL']
        access_token = create_access_token(identity=email)
        return make_response(jsonify({'access_token': access_token, 'admin': is_admin})), OK
    else:
        # Invalid credentials
        return jsonify({'error': 'Invalid credentials'}), UNAUTHORIZED

# @app.route('/', methods=['GET'])
# @jwt_required()
# def main_page():
#     current_user = get_jwt_identity()
#     print(current_user)
#     return make_response(f"Hey {current_user}"), OK

@app.route('/data', methods=['GET'])
@jwt_required()
def get_history_of_user():
    email = get_jwt_identity()
    user = user_service.find_user_by_email(email)
    preds = predictions_service.find_predictions(user.id)
    resources = [media_service.find_resource_by_id(p.source_image_id) for p in preds]
    if not user.is_authorized:
        return make_response(), REFUSED
    return make_response(jsonify({"images": [security_service.encrypt_resource(img.file_path) for img in resources]})), OK

@app.route('/images/<name>')
def get_image(name):
    # Set the directory path where the images are stored
    image_directory = 'images'
    name = security_service.decrypt_resource(name)
    # Serve the image file from the specified directory
    return send_from_directory(image_directory, name.decode())

@app.route('/images', methods=['POST'])
@jwt_required()
def upload_image():
    email = get_jwt_identity()
    user = user_service.find_user_by_email(email)
    file = request.files['files']
    image = Image.open(BytesIO(file.read()))
    path = f'images/{email}_{int(time.time())}.png'
    image.save(path)
    media_service.save_image(user.id, path)
    # image.show()
    return make_response(path), 200

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

@app.route('/inference', methods=['POST'])
@jwt_required()
def inference():
    # file = request.files['files']  # Get the uploaded file from request.files
    # image = Image.open(BytesIO(file.read()))  # Open the image using PIL
    # Process the image as needed
    # ...
    # image.show()
    vals = request.json
    email = get_jwt_identity()
    user = user_service.find_user_by_email(email)
    source_image = media_service.find_resource_by_path(vals['image_path'])
    vals['video_path'] = model_client.predict(**vals)
    media_service.save_video(user.id, vals['video_path'])
    video = media_service.find_resource_by_path(vals['video_path'])
    predictions_service.save_prediction(user_id=user.id,
                                        source_image_id=source_image.id,
                                        output_video_id=video.id,
                                        prompt=vals['prompt'],
                                        motion_filed_strength_x=vals['motion_field_strength_x'],
                                        motion_filed_strength_y=vals['motion_field_strength_y'],
                                        t0=vals['t0'],
                                        t1=vals['t1'],
                                        n_prompt=vals['n_prompt'],
                                        seed=vals['seed'])
    return make_response(security_service.encrypt_resource(vals['video_path'])), OK

if __name__ == '__main__':
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('localhost', 8000))
    # sock.listen(1)
    # print('Service B is listening...')
    app.run(debug=True, port=5000)
