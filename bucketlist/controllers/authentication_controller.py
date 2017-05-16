"""
File      : authentication_controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Controller file handles access and authorization
"""

# ============================================================================
# necessary imports
# ============================================================================
import os
import hashlib
import json
from functools import wraps

from flask import request, make_response, jsonify
import jwt

from datetime import datetime, timedelta

from bucketlist.controllers.database_controller import DatabaseController

TOKEN_HEADER_NAME = "TOKEN"

JWT_SECRET_TOKEN = os.environ['BUCKETLIST_SECRET_KEY']


def encode_auth_token(user_id):
    """
    Generates and encodes the JWT authentication token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=3600),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            JWT_SECRET_TOKEN,
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
        payload = jwt.decode(auth_token, JWT_SECRET_TOKEN)
        data = {'status': True, 'decode_data': payload['sub']}
        return data
    except jwt.ExpiredSignatureError:
        data = {'status': False, 'decode_data': 'Signature expired. Please log in again.'}
        return data
    except jwt.InvalidTokenError:
        data = {'status': False, 'decode_data': 'Invalid token. Please log in again.'}
        return data


def check_token(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        decode = decode_auth_token(request.headers[TOKEN_HEADER_NAME])
        if decode['status'] is False:
            data = {
                'STATUS': 'fail',
                'MESSAGE': decode['decode_data']
            }
            resp = make_response(jsonify(data), 401)
            resp.headers["BUCKET-LIST-APP-ERROR-CODE"] = 9500
            resp.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = decode['decode_data']
            return resp
        return func(*args, **kwargs)
    return decorated
