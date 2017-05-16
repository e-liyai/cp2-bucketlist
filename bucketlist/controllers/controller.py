"""
File      : controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Controller file processes request from the api endpoints
"""

# ============================================================================
# necessary imports
# ============================================================================
import os
import hashlib
import json

from math import ceil
from datetime import datetime

from flask import jsonify, request, abort, make_response, session
from flask_login import login_required, login_user, logout_user, current_user

from bucketlist.app import login_manager
from bucketlist.controllers.database_controller import DatabaseController
from bucketlist.controllers.authentication_controller import encode_auth_token, check_token, decode_auth_token

#
# Database engine
# Postgres connection postgresql+psycopg2://user:password@host/database
#
db_engine = os.environ['BUCKETLIST_SQLALCHEMY_DATABASE_URI']

PAGE_SIZE = 2

DATA_CONTROLLER = DatabaseController(db_engine)


def initialize_database():
    """

    The method initializes tables and relations in the database.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.initialize_database()


def populate_database():
    """

    The method populates database tables with valid data.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.populate_database()


def drop_tables():
    """

    The method drops tables and relations in the database.

    :param : None
    :return: None
    """
    DATA_CONTROLLER.drop_tables()

def login():
    """

    The method validates user credentials and gives user access. The json is hashed to increase security.

    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """

    data = request.data
    data_dict = json.loads(data)

    username = data_dict['username']
    password = data_dict['password']

    try:
        validation_return = DATA_CONTROLLER.user_login_authentication(username=username, password=password)
        if validation_return['status'] is True:
            user = validation_return['User']
            login_user(user, remember=True)
            session['user_id'] = user.user_id

            auth_token = encode_auth_token(user.user_id)

            if auth_token:
                response_data = {
                    'STATUS': 'success',
                    'MESSAGE': 'Successfully logged in.',
                    'TOKEN': auth_token
                }
                data_response = make_response(jsonify(response_data), 200)
                data_response.headers['STATUS'] = 'success'
                data_response.headers['TOKEN'] = auth_token
                return data_response
        else:
            response_data = {
                'STATUS': 'fail',
                'MESSAGE': 'Username or password provided does not match.'
            }
            return make_response(jsonify(response_data)), 401

    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["STATUS"] = 'fail'
        return tmp_response


@check_token
def users(user_id=None, serialize=True):
    """

    The method returns users in a json responses. The json is hashed to increase security.

    :param serialize: Serialize helps indicate the format of the response
    :param user_id: user id intended to be searched
    :return: Json format or plain text depending in the serialize parameter
    """
    users = DATA_CONTROLLER.get_user_by_id(user_id=user_id, serialize=True)
    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(users)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return make_response("", 404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        users = users[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    if serialize:
        data = {
            "users": users,
            "total": len(users),
            "pages": pages
        }
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)

        # Caching
        response.headers["ETag"] = str(hashlib.sha256(json_data).hexdigest())

        # Entity tag uniquely identifies request
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return users


def add_user():
    data = request.data
    data_dict = json.loads(data)

    first_name = data_dict["first_name"]
    last_name = data_dict["last_name"]
    email = data_dict["email"]
    username = data_dict["username"]
    password = data_dict["password"]

    try:
        new_user = DATA_CONTROLLER.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               username=username,
                                               password=password)

        response_data = {
                        'STATUS': 'success',
                        'MESSAGE': 'Successfully registered.',
                        'USER': new_user
                    }

        data_response = make_response(jsonify(response_data), 201)
        data_response.headers['STATUS'] = 'success'
        return data_response
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["STATUS"] = 'fail'
        return tmp_response


@check_token
def user_by_id(user_id):
    """

    The method returns user with provided user_id in a json responses.

    :param user_id: user id of the user to be searched
    :return: User json response
    """
    current_user = DATA_CONTROLLER.get_user_by_id(user_id, serialize=True)
    if current_user:
        return jsonify({"user": current_user})
    else:
        """
        if user with id is not found 404 page is returned
        """
        abort(404)
        return jsonify({
            'STATUS': 'Fail',
            'MESSAGE': 'User with provided id does not exist',
        })


@check_token
def update_user(user_id):
    """

    The method updates user with provided user_id, and returns a json responses.

    :param user_id: user id of the user to be updated
    :return: User json response
    """

    data = request.data
    data_dict = json.loads(data)

    new_user = {
        "first_name": data_dict["first_name"],
        "last_name": data_dict["last_name"],
        "email": data_dict["email"],
        "username": data_dict["username"]
    }
    updated_user = DATA_CONTROLLER.update_user(user_id, new_user)
    if not updated_user:
        data = {
            "STATUS": 'fail',
            "MESSAGE": 'Error updating user'
        }
        response = make_response(jsonify(data), 500)
        return response
    else:
        data = {
            "STATUS": 'success',
            "updated_user": updated_user
        }
        response = make_response(jsonify(data), 201)
        return response


@check_token
def delete_user(user_id):
    """

    The method deletes user with provided user_id.

    :param user_id: user id of the user to be deleted
    :return: http response
    """
    try:
        if DATA_CONTROLLER.delete_user(user_id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        return tmp_response


@check_token
def create_bucketlist():
    """

    The method adds a new bucketlist under the current user.

    :param : None
    :return: http response 
    """

    try:
        data = request.data
        data_dict = json.loads(data)

        bucketlist_name = data_dict["name"]
        user = current_user

        auth_token = request.headers.get('TOKEN')
        resp = decode_auth_token(auth_token)

        if not resp['status']:
            data = {
                'STATUS': 'fail',
                'MESSAGE': 'Invalid token provided'
            }
            data_response = make_response(jsonify(data), 401)
            data_response.headers['STATUS'] = 'success'
            return data_response

        new_bucket_name = DATA_CONTROLLER.create_bucketlist(bucketlist_name, resp['decode_data'])

        response_data = {
            'STATUS': 'success',
            'MESSAGE': 'Bucket list successfully created.',
            'BUCKET_LIST_NAME': new_bucket_name
        }

        data_response = make_response(jsonify(response_data), 201)
        data_response.headers['STATUS'] = 'success'
        return data_response
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["STATUS"] = 'fail'
        return tmp_response


@check_token
def bucketlist(bucket_id=None, serialize=True):
    """

    The method returns bucketlist in a json responses.

    :param bucket_id: id of bucket list to be retrieved
    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """

    auth_token = request.headers.get('TOKEN')

    if auth_token:
        resp = decode_auth_token(auth_token)
        if resp['status']:
            if resp['decode_data']:

                bucketlists = DATA_CONTROLLER.get_bucketlist_by_id(bucket_id=bucket_id, user=resp['decode_data'],
                                                                   serialize=True)

                page = request.args.get("limit")
                number_of_pages = None
                pages = []
                if page:
                    number_of_pages = int(ceil(float(len(bucketlists)) / PAGE_SIZE))
                    converted_page = int(page)

                    if converted_page > number_of_pages or converted_page < 0:
                        return make_response("", 404)

                    from_index = (converted_page - 1) * PAGE_SIZE
                    to_index = from_index + PAGE_SIZE

                    bucketlists = bucketlists[from_index:to_index]
                    if number_of_pages:
                        pages = range(1, number_of_pages+1)

                if serialize:
                    data = {
                        'STATUS': 'success',
                        "bucketlists": bucketlists,
                        "total": len(bucketlists),
                        "pages": pages
                    }
                    json_data = json.dumps(data)
                    response = make_response(jsonify(data), 200)
                    response.headers["ETag"] = str(hashlib.sha256(json_data).hexdigest())
                    response.headers["Cache-Control"] = "private, max-age=300"
                    return response
                else:
                    return bucketlists
    else:
        response_object = {
            'STATUS': 'fail',
            'MESSAGE': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 401


@check_token
def update_bucketlist(bucket_id):
    """

    The method updates bucket list with provided the id, and returns a json responses.

    :param bucket_id: id of the bucket list to be updated
    :return: bucket list json response
    """

    data = request.data
    data_dict = json.loads(data)

    auth_token = request.headers.get('TOKEN')
    resp = decode_auth_token(auth_token)
    if not resp['status']:
        data = {
            'STATUS': 'fail',
            'MESSAGE': 'Invalid token provided'
        }
        data_response = make_response(jsonify(data), 401)
        data_response.headers['STATUS'] = 'success'
        return data_response

    new_bucket = {
        "bucketlist_name": data_dict["name"]
    }
    updated_bucket = DATA_CONTROLLER.update_bucketlist(bucket_id=bucket_id, new_bucketlist=new_bucket,
                                                       user=resp['decode_data'])
    if updated_bucket:
        data = {
            'STATUS': 'success',
            'bucketlist': updated_bucket
        }
        data_response = make_response(jsonify(data), 201)
        data_response.headers['STATUS'] = 'success'
        return data_response
    else:
        tmp_response = make_response("", 500)
        return tmp_response


@check_token
def delete_bucketlist(bucket_id):
    """

    The method deletes bucket list with provided id.

    :param bucket_id: id of the bucket list to be deleted
    :return: http response
    """
    try:
        if DATA_CONTROLLER.delete_bucketlist(bucket_id):
            data = {
                'STATUS': 'Success',
                'MESSAGE': 'Database with id '+bucket_id+' successfully deleted'
            }
            data_response = make_response(jsonify(data), 200)
            data_response.headers['STATUS'] = 'success'
            return data_response
        else:
            data = {
                'STATUS': 'Error',
                'MESSAGE': 'Bucketlist ID cannot be found, or database encountered an error.'
            }
            data_response = make_response(jsonify(data), 500)
            data_response.headers['STATUS'] = 'fail'
            return data_response
    except ValueError as err:
        tmp_response = make_response("", 500)
        return tmp_response


@check_token
def item(item_id=None, bucket_id=None, serialize=True):
    """

    The method returns items in a json responses.

    :param item_id: id of item to be retrieved
    :param bucket_id: id of bucket list to which the item belongs
    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """
    items = DATA_CONTROLLER.get_item_by_id(item_id=item_id, bucket_id=bucket_id, serialize=True)

    if item_id:

        if not items:
            data = {
                'STATUS': 'fail',
                'MESSAGE': 'The user has no item with provided ID in any of the bucket lists'
            }
            data_response = make_response(jsonify(data), 404)
            data_response.headers['STATUS'] = 'fail'
            return data_response

    page = request.args.get("limit")
    number_of_pages = None
    pages = []
    if page:
        number_of_pages = int(ceil(float(len(items)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return make_response("", 404)

        from_index = (converted_page - 1) * PAGE_SIZE
        to_index = from_index + PAGE_SIZE

        items = items[from_index:to_index]
        if number_of_pages:
            pages = range(1, number_of_pages + 1)

    if serialize:
        data = {
            "bucketlist_item": items,
            "total": len(items),
            "pages": pages
        }
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)
        response.headers["ETag"] = str(hashlib.sha256(json_data).hexdigest())
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return items


@check_token
def create_item(bucket_id):
    """

    The method adds a new item under the current bucket list.

    :param bucket_id: id of the bucket list to be deleted
    :return: http response 
    """
    data = request.data
    data_dict = json.loads(data)

    item_name = data_dict["name"]
    item_description = data_dict["description"]

    new_item_name = DATA_CONTROLLER.create_bucketlist_item(item_name, item_description, bucket_id)
    data = {
        "STATUS": 'success',
        "bucket_list_item": new_item_name
    }
    response = make_response(jsonify(data), 201)
    return response


@check_token
def update_item(item_id):
    """

    The method updates item with provided the id, and returns a json responses.

    :param item_id: id of the item to be updated
    :return: item json response
    """
    data = request.data
    data_dict = json.loads(data)

    date_completed = None
    done = False
    if data_dict["done"] == 'True':
        done = True
        date_completed = datetime.now()

    new_item = {
        "item_name": data_dict["name"],
        "done": done,
        "description": data_dict["description"],
        "date_completed": date_completed
    }

    updated_item = DATA_CONTROLLER.update_bucketlist_item(item_id, new_item)
    if not updated_item:
        data = {
            "STATUS": 'fail',
            "MESSAGE": 'Error updating item'
        }
        response = make_response(jsonify(data), 500)
        return response
    else:
        data = {
            "STATUS": 'success',
            "bucket_list_item": updated_item
        }
        response = make_response(jsonify(data), 201)
        return response


@check_token
def delete_item(item_id):
    """

    The method deletes item with the provided id.

    :param item_id: id of the item to be deleted
    :return: http response
    """
    try:
        if DATA_CONTROLLER.delete_bucketlist_item(item_id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        return tmp_response


@check_token
def search(search_value):
    """

    The search method searches bucket list database.

    :param search_value: value to be searched
    :return: http response
    """
    auth_token = request.headers.get('TOKEN')
    resp = decode_auth_token(auth_token)
    if not resp['status']:
        data = {
            'STATUS': 'fail',
            'MESSAGE': 'Invalid token provided'
        }
        data_response = make_response(jsonify(data), 401)
        data_response.headers['STATUS'] = 'fail'
        return data_response

    search_result = DATA_CONTROLLER.search_database(search_value, resp['decode_data'], serialize=True)

    if search_result:
        response_data = {
            'STATUS': 'success',
            'SEARCH': search_result
        }

        data_response = make_response(jsonify(response_data), 200)
        data_response.headers['STATUS'] = 'success'
        return data_response
    else:
        response_data = {
            'STATUS': 'fail',
            'MESSAGE': 'No bucket list with search phrase found'
        }

        data_response = make_response(jsonify(response_data), 404)
        data_response.headers['STATUS'] = 'fail'
        return data_response


def authenticate():
    auth_token = request.headers.get('TOKEN')
    resp = decode_auth_token(auth_token)

    if resp['status']:
        response_data = {
            'STATUS': 'success',
            'MESSAGE': 'Authenticated'
        }

        data_response = make_response(jsonify(response_data), 200)
        data_response.headers['STATUS'] = 'success'
        return data_response
    else:
        response_data = {
            'STATUS': 'fail',
            'MESSAGE': 'Not authenticated'
        }

        data_response = make_response(jsonify(response_data), 401)
        data_response.headers['STATUS'] = 'fail'
        return data_response
