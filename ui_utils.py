from flask import request


def get_authorization_header(headers=None):
    headers_object = {} if headers is None else headers
    headers_object['Authorization'] = f'Bearer {get_token_from_cookie()}'
    return headers_object


def has_cookie():
    return False if get_token_from_cookie() is None else True


def get_token_from_cookie():
    return request.cookies.get('session_token')