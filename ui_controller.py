from flask import Flask, request, jsonify, make_response, render_template, Response
import requests
from flask_cors import CORS

from ui_utils import has_cookie, fetch_data, redirect_to_page_with_cookie, redirect_to_page, get_token_from_cookie, \
    fetch_admin_data, update_authorization
from comm_utils import OK, UNAUTHORIZED, REFUSED, BAD_REQUEST

app = Flask(__name__)
CORS(app)
BACKEND_URL = 'http://localhost:5000'  # Replace with your backend service URL

@app.route('/', methods=['GET'])
def main_page():
    if not has_cookie():
        return redirect_to_page('/login')
    data = fetch_data()
    if data == UNAUTHORIZED:
        return redirect_to_page_with_cookie('/login', value='', expires=0)
    if data == REFUSED:
        return render_template('pending.html', message = 'You are in the queue, pending admin authorization. Thank you for your patience!')
    return render_template('main.html', images=[f'http://localhost:7246/images/{img}' for img in data])

@app.route('/gradio', methods=['GET'])
def get_inference():
    response = make_response(render_template('gradio.html'))
    return response


@app.route('/login', methods=['POST', 'GET'])
def login():
    if has_cookie():
        return redirect_to_page('/')
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    response = requests.post(f'{BACKEND_URL}/login', json={'email': email, 'password': password})
    if response.status_code == OK:
        session_token = response.json().get('access_token')
        is_admin = bool(response.json().get('admin'))
        if is_admin:
            return redirect_to_page_with_cookie('/admin', cookie_name='admin_session_token', value=session_token)
        return redirect_to_page_with_cookie('/', value=session_token)

    return render_template('login.html', message="Invalid credentials!")


@app.route('/images/<name>', methods=['GET'])
def get_image(name):
    #TODO - input sanitization
    response = requests.get(f'{BACKEND_URL}/images/{name}')
    if response.status_code == OK:
        return Response(response.content, headers={'Content-Type': 'image/png'})
    else:
        return ""
@app.route('/admin', methods=['GET'])
def get_admin_page():
    if not has_cookie():
        return redirect_to_page('/login')
    data = fetch_admin_data()
    if data is None:
        return "UNAUTHORIZED ADMIN ACCESS!"
    return render_template('admin.html', users=data)


@app.route('/admin/authorizations', methods=['PUT'])
def get_update_authorization():
    if not has_cookie():
        return redirect_to_page('/login')
    email = request.json.get('email')
    authorization = request.json.get('authorization')
    print(email, authorization)
    status = update_authorization(email, authorization)
    return make_response(), status

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        response = requests.post(f'{BACKEND_URL}/signup', json={'email': username, 'password': password})
        if response.status_code == 200:
            return redirect_to_page('/login')
        else:
            return make_response(jsonify({'error': 'Invalid credentials'}), 401)
    elif has_cookie():
        return redirect_to_page('/')
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(debug=True, port=7246)
