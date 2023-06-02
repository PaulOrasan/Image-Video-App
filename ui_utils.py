from flask import request, redirect, jsonify
import requests

from comm_utils import OK

BACKEND_URL = 'http://localhost:5000'

SESSION_COOKIE_NAME = 'session_token'
ADMIN_SESSION_COOKIE_NAME = 'admin_session_token'


def get_authorization_header(headers=None):
    headers_object = {} if headers is None else headers
    headers_object['Authorization'] = f'Bearer {get_token_from_cookie()}'
    return headers_object


def has_cookie():
    return False if get_token_from_cookie() is None else True


def get_token_from_cookie():
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        token = request.cookies.get(ADMIN_SESSION_COOKIE_NAME)
    return token

def fetch_data():
    headers = get_authorization_header()
    response = requests.get(f'{BACKEND_URL}/data', headers=headers)
    if response.status_code == OK:
        # TODO - check wrong json
        return response.json().get('images')
    return response.status_code

def fetch_admin_data():
    headers = get_authorization_header()
    response = requests.get(f'{BACKEND_URL}/admin', headers=headers)
    if response.status_code == 200:
        return response.json().get('data')
    return None

def update_authorization(email: str, authorization_status: bool):
    headers = get_authorization_header()
    response = requests.put(f'{BACKEND_URL}/admin/authorizations', headers=headers,
                            json={'email': email, 'authorization': authorization_status})
    return response.status_code

def redirect_to_page(redirect_path):
    return redirect_to_page_with_cookie(redirect_path, cookie_name=None)


def redirect_to_page_with_cookie(redirect_path,
                                 cookie_name=SESSION_COOKIE_NAME,
                                 value='',
                                 http_only=True,
                                 expires='Session'):
    response = redirect(redirect_path)
    if cookie_name is not None:
        response.set_cookie(cookie_name, value, httponly=http_only, expires=expires)
    return response
