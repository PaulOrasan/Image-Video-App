import requests
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette import status

from comm_utils import OK

BACKEND_URL = 'http://localhost:5000'

SESSION_COOKIE_NAME = 'session_token'
ADMIN_SESSION_COOKIE_NAME = 'admin_session_token'


def get_authorization_header(request: Request, headers=None):
    headers_object = {} if headers is None else headers
    headers_object['Authorization'] = f'Bearer {get_token_from_cookie(request)}'
    return headers_object


def has_cookie(request: Request):
    return False if get_token_from_cookie(request) is None else True

def get_cookie_name(request:Request):
    if hasattr(request, 'cookies'):
        if SESSION_COOKIE_NAME in request.cookies:
            return SESSION_COOKIE_NAME
        if ADMIN_SESSION_COOKIE_NAME in request.cookies:
            return ADMIN_SESSION_COOKIE_NAME
    else:
        # token = list(filter(lambda x: x.strip().startswith(SESSION_COOKIE_NAME), request.headers.cookie.split(';')))[0].split('=')[1]
        if SESSION_COOKIE_NAME in request.headers.cookie:
            return SESSION_COOKIE_NAME
        if ADMIN_SESSION_COOKIE_NAME in request.headers.cookie:
            return ADMIN_SESSION_COOKIE_NAME
def has_authorization(request: Request):
    return request.headers.get('authorization', None)
def get_token_from_cookie(request: Request):
    # token = request.cookies.get(SESSION_COOKIE_NAME)
    if hasattr(request, 'cookies'):
        if SESSION_COOKIE_NAME in request.cookies:
            return request.cookies[SESSION_COOKIE_NAME]
        if ADMIN_SESSION_COOKIE_NAME in request.cookies:
            return request.cookies[ADMIN_SESSION_COOKIE_NAME]
    else:
        # token = list(filter(lambda x: x.strip().startswith(SESSION_COOKIE_NAME), request.headers.cookie.split(';')))[0].split('=')[1]
        if SESSION_COOKIE_NAME in request.headers.cookie:
            return list(filter(lambda x: x.strip().startswith(SESSION_COOKIE_NAME), request.headers.cookie.split(';')))[0].split('=')[1]
        if ADMIN_SESSION_COOKIE_NAME in request.headers.cookie:
            return list(filter(lambda x: x.strip().startswith(ADMIN_SESSION_COOKIE_NAME), request.headers.cookie.split(';')))[0].split('=')[1]
    # if not token:
    #     token = request.cookies.get(ADMIN_SESSION_COOKIE_NAME)
    # return token


def fetch_data(request: Request):
    headers = get_authorization_header(request)
    response = requests.get(f'{BACKEND_URL}/data', headers=headers)
    if response.status_code == OK:
        # TODO - check wrong json
        return response.json()
    return response.status_code


def fetch_admin_data(request: Request):
    headers = get_authorization_header(request)
    response = requests.get(f'{BACKEND_URL}/admin', headers=headers)
    if response.status_code == 200:
        return response.json().get('data')
    return None


def update_authorization(request: Request, email: str, authorization_status: bool):
    headers = get_authorization_header(request)
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
    response = RedirectResponse(redirect_path, status_code=status.HTTP_302_FOUND)
    if cookie_name is not None:
        response.set_cookie(cookie_name, value, httponly=http_only, expires=expires)
    return response
