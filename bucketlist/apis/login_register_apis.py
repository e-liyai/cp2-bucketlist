"""
File      : login_register_apis.py
Date      : April, 2017
Author    : eugene liyai
Desc      : bucket list authentication apis
"""

# ============================================================================
# necessary imports
# ============================================================================
from functools import wraps
from flask import request
from flask import make_response


def validate_user(username=None, email=None, password=None):
    if username and password:
        return username and password
    elif email and password:
        return email and password


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not validate_user(username=auth.username, password=auth.password) or not \
                validate_user(email=auth.email, password=auth.password):
            auth_response = make_response("", 401)
            auth_response.headers["WWW-Authenticate"] = 'Basic realm="Login required"'
            return auth_response

        return func(*args, **kwargs)
    return decorated
