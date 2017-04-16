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

from bucketlist.controllers.database_controller import DatabaseController

TOKEN = hashlib.sha256("SAMPLE UNIQI TOKEN FOR USER").hexdigest()
TOKEN_HEADER_NAME = "MY_AUTH_TOKEN"


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