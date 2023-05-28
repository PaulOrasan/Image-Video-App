from flask import Flask, request, jsonify, make_response, render_template, redirect
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
BACKEND_URL = 'http://localhost:5000'  # Replace with your backend service URL

@app.route('/', methods=['GET'])
def main_page():
    if request.cookies.get('session_token'):
        token =  request.cookies.get('session_token')
        print("GOT COOKIE", token)
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{BACKEND_URL}/', headers=headers)
        if response.status_code == 200:
            return render_template('main.html', data=response.text)
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
    # Get username and password from the request
        username = request.form.get('username')
        password = request.form.get('password')

        # Send a request to the backend login service
        response = requests.post(f'{BACKEND_URL}/login', json={'username': username, 'password': password})

        if response.status_code == 200:
            # Backend validation successful
            # Generate a secure session token or cookie
            session_token = response.json().get('access_token')

            # Set the session token in the response cookie
            # response = make_response(jsonify({'message': 'Login successful'}))
            response = make_response(redirect('/'))
            response.set_cookie('session_token', session_token, httponly=True)

            return response
        else:
            # Backend validation failed
            return make_response(jsonify({'error': 'Invalid credentials'}), 401)
    elif request.cookies.get('session_token'):
        return redirect('/')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=7246)
