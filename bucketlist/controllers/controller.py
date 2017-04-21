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

from flask import jsonify, request, abort, make_response
from flask_login import login_required, login_user, logout_user, current_user

from bucketlist.app import login_manager
from bucketlist.controllers.database_controller import DatabaseController
from bucketlist.controllers.authentication_controller import encode_auth_token, check_token, decode_auth_token

BUCKETLIST_DATABASE = os.environ['BUCKETLIST_SQLALCHEMY_DATABASE_URI']

#
# Database engine
# Postgres connection postgresql+psycopg2://user:password@host/database
#
db_engine = 'postgresql+psycopg2://admin:admin@localhost/bucketlist'

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


def build_message(key, message):
    """

    The method returns key value json format messages

    :param : None
    :return: None
    """
    return {key: message}


@login_manager.user_loader
def load_user(user_id):
    return DATA_CONTROLLER.get_user_by_id(user_id)


def login():
    """

    The method validates user credentials and gives user access. The json is hashed to increase security.

    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """
    username = request.form['username']
    password = request.form['password']

    try:
        validation_return = DATA_CONTROLLER.user_login_authentication(username=username, password=password)
        if validation_return['status'] is True:
            user = validation_return['User']
            login_user(user, True)

            auth_token = encode_auth_token(user.user_id)

            if auth_token:
                response_data = {
                    'STATUS': 'success',
                    'MESSAGE': 'Successfully logged in.'
                }
                data_response = make_response(jsonify(response_data), 200)
                data_response.headers['STATUS'] = 'success'
                data_response.headers['TOKEN'] = auth_token
                return data_response
        else:
            response_data = {
                'STATUS': 'fail',
                'MESSAGE': 'User does not exist.'
            }
            return make_response(jsonify(response_data)), 404

    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["STATUS"] = 'fail'
        tmp_response.headers["BUCKET-LIST-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = err.message
        return tmp_response


def users(serialize=True):
    """

    The method returns users in a json responses. The json is hashed to increase security.

    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """
    users = DATA_CONTROLLER.get_user_by_id(serialize=True)
    page = request.args.get("limit")
    if page:
        number_of_pages = int(ceil(float(len(users)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return make_response("", 404)

        from_index = converted_page * PAGE_SIZE - 1
        to_index = from_index + PAGE_SIZE

        users = users[from_index:to_index]

    if serialize:
        data = {"users": users, "total": len(users)}
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)

        # Caching
        response.headers["ETag"] = str(hashlib.sha256(json_data).hexdigest())  # Entity tag uniquely identifies request
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return users


def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    try:
        new_user = DATA_CONTROLLER.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               username=username,
                                               password=password)

        # generate the auth token
        auth_token = encode_auth_token(new_user['user_id'])

        return jsonify({
                        'STATUS': 'success',
                        'MESSAGE': 'Successfully registered.',
                        'AUTH_TOKEN': auth_token.decode(),
                        'USER': new_user
                    })
    except ValueError as err:
        tmp_response = make_response("", 401)
        tmp_response.headers["STATUS"] = 'fail'
        tmp_response.headers["BUCKET-LIST-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = err.message
        return tmp_response


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


def update_user(user_id):
    """

    The method updates user with provided user_id, and returns a json responses.

    :param user_id: user id of the user to be updated
    :return: User json response
    """
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "username": request.form["username"]
    }
    updated_user = DATA_CONTROLLER.update_user(user_id, new_user)
    if not updated_user:
        return make_response('', 204)
    else:
        return jsonify({"user": updated_user})


def get_error_code(error):
    if "parameter" in error.message.lower():
        return 8100

    return 8000


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
        tmp_response.headers["BUCKET-LIST-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = err.message
        return tmp_response


def create_bucketlist():
    """

    The method adds a new bucketlist under the current user.

    :param : None
    :return: http response 
    """
    bucketlist_name = request.form["name"]
    user = current_user

    new_bucket_name = DATA_CONTROLLER.create_bucketlist(bucketlist_name, user[0].user_id)

    return jsonify({
        "bucket_name": new_bucket_name
    })


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
            if current_user[0].user_id == resp['decode_data']:

                bucketlists = DATA_CONTROLLER.get_bucketlist_by_id(bucket_id=bucket_id, serialize=True)

                page = request.args.get("limit")
                if page:
                    number_of_pages = int(ceil(float(len(bucketlists)) / PAGE_SIZE))
                    converted_page = int(page)

                    if converted_page > number_of_pages or converted_page < 0:
                        return make_response("", 404)

                    from_index = converted_page * PAGE_SIZE - 1
                    to_index = from_index + PAGE_SIZE

                    bucketlists = bucketlists[from_index:to_index]

                if serialize:
                    data = {
                        'STATUS': 'success',
                        "bucketlists": bucketlists,
                        "total": len(bucketlists)
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


def update_bucketlist(bucket_id):
    """

    The method updates bucket list with provided the id, and returns a json responses.

    :param bucket_id: id of the bucket list to be updated
    :return: bucket list json response
    """
    new_bucket = {
        "bucketlist_name": request.form["name"]
    }
    updated_bucket = DATA_CONTROLLER.update_bucketlist(bucket_id, new_bucket)
    if not updated_bucket:
        return make_response('', 204)
    else:
        return jsonify({"bucket_list": updated_bucket})


def delete_bucketlist(bucket_id):
    """

    The method deletes bucket list with provided id.

    :param bucket_id: id of the bucket list to be deleted
    :return: http response
    """
    try:
        if DATA_CONTROLLER.delete_bucketlist(bucket_id):
            return make_response("", 200)
        else:
            return make_response("", 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = err.message
        return tmp_response


def item(item_id=None, serialize=True):
    """

    The method returns items in a json responses.

    :param item_id: id of item to be retrieved
    :param serialize: Serialize helps indicate the format of the response
    :return: Json format or plain text depending in the serialize parameter
    """
    items = DATA_CONTROLLER.get_item_by_id(item_id=item_id, serialize=True)
    page = request.args.get("limit")
    if page:
        number_of_pages = int(ceil(float(len(items)) / PAGE_SIZE))
        converted_page = int(page)

        if converted_page > number_of_pages or converted_page < 0:
            return make_response("", 404)

        from_index = converted_page * PAGE_SIZE - 1
        to_index = from_index + PAGE_SIZE

        items = items[from_index:to_index]

    if serialize:
        data = {"bucketlists": items, "total": len(items)}
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)
        response.headers["ETag"] = str(hashlib.sha256(json_data).hexdigest())
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return items


def create_item(bucket_id):
    """

    The method adds a new item under the current bucket list.

    :param bucket_id: id of the bucket list to be deleted
    :return: http response 
    """
    item_name = request.form["name"]
    item_description = request.form["description"]

    new_item_name = DATA_CONTROLLER.create_bucketlist_item(item_name, item_description, bucket_id)

    return jsonify({
        "item_name": new_item_name
    })


def update_item(item_id):
    """

    The method updates item with provided the id, and returns a json responses.

    :param item_id: id of the item to be updated
    :return: item json response
    """

    date_completed = None
    done = False
    if request.form["done"] == 'True':
        done = True
        date_completed = datetime.now()

    new_item = {
        "item_name": request.form["name"],
        "done": done,
        "description": request.form["description"],
        "date_completed": date_completed
    }

    updated_item = DATA_CONTROLLER.update_bucketlist_item(item_id, new_item)
    if not updated_item:
        return make_response('', 204)
    else:
        return jsonify({"bucket_list_item": updated_item})


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
        tmp_response.headers["BUCKET-LIST-APP-ERROR-CODE"] = get_error_code(err)
        tmp_response.headers["BUCKET-LIST-APP-ERROR-MESSAGE"] = err.message
        return tmp_response
