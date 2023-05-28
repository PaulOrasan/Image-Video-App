from flask import Flask, request, jsonify, make_response, render_template, redirect, Response
import requests
from flask_cors import CORS

from ui_utils import has_cookie, get_authorization_header

app = Flask(__name__)
CORS(app)
BACKEND_URL = 'http://localhost:5000'  # Replace with your backend service URL

@app.route('/', methods=['GET'])
def main_page():
    if has_cookie():
        headers = get_authorization_header()
        response = requests.get(f'{BACKEND_URL}/history', headers=headers)
        if response.status_code == 200:
            #TODO - check wrong json
            imgs = response.json().get('images')
            return render_template('main.html', images=[f'http://localhost:7246/images/{img}' for img in imgs])
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        response = requests.post(f'{BACKEND_URL}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session_token = response.json().get('access_token')
            response = make_response(redirect('/'))
            response.set_cookie('session_token', session_token, httponly=True)
            return response
        else:
            return make_response(jsonify({'error': 'Invalid credentials'}), 401)
    elif request.cookies.get('session_token'):
        return redirect('/')
    return render_template('login.html')

@app.route('/images/<name>')
def get_image(name):
    #TODO - input sanitization
    response = requests.get(f'{BACKEND_URL}/images/{name}')
    if response.status_code == 200:
        return Response(response.content, headers={'Content-Type': 'image/png'})
    else:
        return ""
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=7246)
