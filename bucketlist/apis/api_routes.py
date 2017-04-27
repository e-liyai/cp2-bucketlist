"""
File      : api_routes.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Routing api endpoints
"""
# ============================================================================
# necessary imports
# ============================================================================
from flask import jsonify

from bucketlist.controllers.controller import add_user, users, delete_user, update_user
from bucketlist.controllers.controller import create_bucketlist, bucketlist, update_bucketlist, delete_bucketlist
from bucketlist.controllers.controller import create_item, update_item, delete_item, login, item


def initialize_api_routes(app):
    if app:
        app.add_url_rule('/auth/register/', 'add_user', add_user, methods=['POST'])
        app.add_url_rule('/auth/login/', 'login', login, methods=['POST'])
        app.add_url_rule('/api/v1/delete_user/<string:user_id>', 'delete_user', delete_user, methods=['DELETE'])
        app.add_url_rule('/api/v1/bucketlists/', 'bucketlist', bucketlist, methods=['GET'])
        app.add_url_rule('/api/v1/users/', 'users', users, methods=['GET'])
        app.add_url_rule('/api/v1/user/<string:user_id>', 'users', users, methods=['GET'])
        app.add_url_rule('/api/v1/user/<string:user_id>', 'update_user', update_user, methods=['PUT'])
        app.add_url_rule('/api/v1/bucketlists/', 'create_bucketlist', create_bucketlist, methods=['POST'])
        app.add_url_rule('/api/v1/bucketlists/<string:bucket_id>', 'bucketlist_by_id', bucketlist, methods=['GET'])
        app.add_url_rule('/api/v1/bucketlists/<string:bucket_id>',
                         'update_bucketlist', update_bucketlist, methods=['PUT'])
        app.add_url_rule('/api/v1/bucketlists/<string:bucket_id>',
                         'delete_bucketlist', delete_bucketlist, methods=['DELETE'])
        app.add_url_rule('/api/v1/bucketlists/<string:bucket_id>/items', 'create_bucketlist_item', create_item,
                         methods=['POST'])
        app.add_url_rule('/api/v1/bucketlists/items/<string:item_id>', 'item', item,
                         methods=['GET'])
        app.add_url_rule('/api/v1/bucketlists/items', 'item', item,
                         methods=['GET'])
        app.add_url_rule('/api/v1/bucketlists/items/<string:item_id>',
                         'update_bucketlist_item', update_item,
                         methods=['PUT'])
        app.add_url_rule('/api/v1/bucketlists/items/<string:item_id>',
                         'delete_bucketlist_item', delete_item,
                         methods=['DELETE'])
        app.add_url_rule('/api/v1/', 'list_app_routes', list_app_routes, methods=['GET'], defaults={'app': app})


def list_app_routes(app):
    result = []
    for app_route in app.url_map.iter_rules():
        result.append({
            'methods': list(app_route.methods),
            'route': str(app_route)
        })
    return jsonify({'routes': result, 'total': len(result)})
