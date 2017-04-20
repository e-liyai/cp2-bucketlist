"""
File      : authentication_controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Controller file handles access and authorization
"""

# ============================================================================
# necessary imports
# ============================================================================
from functools import wraps
from flask import request, make_response
import hashlib
import jwt

from datetime import datetime, timedelta

from bucketlist.controllers.database_controller import DatabaseController

TOKEN = hashlib.sha256("SAMPLE UNIQI TOKEN FOR USER").hexdigest()
TOKEN_HEADER_NAME = "MY_AUTH_TOKEN"


def encode_auth_token(user_id):
    """
    Generates and encodes the JWT authentication token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            '=\xd5\xb5\x88\x80\rc\xaf\xecK/r\x94V\x0fp\xe6\xf9QU\xe2\x8c\xa3\xd0',
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the JWT authentication token
    :param auth_token: encoded authentication token
    :return: user id
    """
    try:
        payload = jwt.decode(auth_token, '=\xd5\xb5\x88\x80\rc\xaf\xecK/r\x94V\x0fp\xe6\xf9QU\xe2\x8c\xa3\xd0')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def authenticate(is_user_valid_func):
    def auth(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not is_user_valid_func(username=auth.username, password=auth.password):
                resp = make_response("", 401)
                resp.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
                return resp
            return func(*args, **kwargs)
        return decorated
    return auth


def check_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.headers[TOKEN_HEADER_NAME] and request.headers[TOKEN_HEADER_NAME] != TOKEN:
            resp = make_response("", 401)
            resp.headers["X-APP-ERROR-CODE"] = 9500
            resp.headers["X-APP-ERROR-MESSAGE"] = "No valid authentication token found in request"
            return resp
        return func(*args, **kwargs)
    return decorated
