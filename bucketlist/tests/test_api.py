"""
File      : test_views.py
Date      : April, 2017
Author    : eugene liyai
Desc      : api test file
"""

# ============================================================================
# necessary imports
# ============================================================================
import json

from unittest import TestCase

from bucketlist.app import app


class APITest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        data = {'username': 'liyai',
                'password': 'password'
                }

        headers = [('Content-Type', 'application/json')]
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        response = self.app.post(
            '/auth/login/',
            data=json_data,
            content_type='text/plain'
        )

        self.data = json.loads(response.data)

    def tearDown(self):
        print('=> Tearing down after test')

    def test_login_fail(self):
        data = {'username': 'liyai',
                'password': 'passsword'
            }
        headers = [('Content-Type', 'application/json')]
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        response = self.app.post(
            '/auth/login/',
            data=json_data,
            content_type='text/plain'
        )
        self.assertEqual(response.status_code, 401)

    def test_get_user_by_id(self):
        print('=> Test get user by id')
        request = self.app.get('/api/v1/user/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(resp_data['total'], 1)

    def test_get_user(self):
        print('=> Test get user by id')
        request = self.app.get('/api/v1/users/?limit=1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(resp_data['total'], 2)

    def test_get_all_bucketlist(self):
        print('=> Test get all bucket lists')
        request = self.app.get('/api/v1/bucketlists/', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(resp_data['STATUS'], 'success')

    def test_bucketlist_pagination(self):
        print('=> Test get all bucket lists')
        request = self.app.get('/api/v1/bucketlists/?limit=1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(resp_data['STATUS'], 'success')

    def test_get_bucketlist_by_id(self):
        print('=> Test get bucket list by id')
        request = self.app.get('/api/v1/bucketlists/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        bucket_list = resp_data['bucketlists'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(bucket_list)

    def test_invalid_authorisation_token(self):
        print('=> Test invalid token')
        request = self.app.get('/api/v1/bucketlists/1', headers={'TOKEN': 'Invalid_token'})
        resp_data = json.loads(request.data)
        message = resp_data['MESSAGE']
        self.assertEqual(request.status_code, 401)
        self.assertEqual(message, 'Invalid token. Please log in again.')

    def test_get_item_by_id(self):
        print('=> Test get bucket list item by id')
        request = self.app.get('/api/v1/bucketlists/items/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        item = resp_data['bucketlist_item'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(item)
        self.assertEqual(item['item_name'], 'Sky diving')

    def test_get_all_items(self):
        print('=> Test get bucket list items')
        request = self.app.get('/api/v1/bucketlists/items/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        item = resp_data['bucketlist_item'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(item)

    def test_get_all_items_in_first_page(self):
        print('=> Test get bucket list items')
        request = self.app.get('/api/v1/bucketlists/items/1?limit=1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        item = resp_data['bucketlist_item'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(item)

    def test_get_items_in_invalid_page(self):
        print('=> Test get bucket list items')
        request = self.app.get('/api/v1/bucketlists/items/1?limit=10', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(request.status_code, 404)

    def test_get_users(self):
        print('=> Test get users')
        request = self.app.get('/api/v1/users/', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        users = resp_data['users'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(users)

    def test_get_user_by_id(self):
        print('=> Test get users')
        request = self.app.get('/api/v1/user/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        user = resp_data['users'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(user)
        self.assertEqual(user['first_name'], 'eugene')

    def test_get_application_urls(self):
        print('=> get urls')
        request = self.app.get('/api/v1/', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        self.assertIsNotNone(resp_data)
        self.assertEqual(request.status_code, 200)

    def test_create_new_user(self):
        print('=> create new user')
        data = {'username': 'Jesse',
                'password': 'password',
                'first_name': 'Mary',
                'last_name': 'Mary',
                'email': 'mary@mail.com'
                }

        json_data = json.dumps(data)
        response = self.app.post('/auth/register/', data=json_data, headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 201)

    def test_update_existing_user(self):
        print('=> Update existing user')
        data = {'username': 'UU',
                'first_name': 'eugene',
                'last_name': 'liyailiyai',
                'email': 'liyail@mail.com'
                }

        json_data = json.dumps(data)
        response = self.app.put('/api/v1/user/1', data=json_data, headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 201)

    def test_delete_user(self):
        print('=> delete user')
        response = self.app.delete('/api/v1/delete_user/3', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_create_bucketlist(self):
        print('=> create bucket list')
        data = {
            'name': 'test_bucket_list'
        }
        json_data = json.dumps(data)
        response = self.app.post('/api/v1/bucketlists/', data=json_data, headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist(self):
        print('=> update bucketlist')
        data = {
            'name': 'updated_test_bucket_list'
        }
        json_data = json.dumps(data)
        response = self.app.put('/api/v1/bucketlists/1', data=json_data, headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 201)

    def test_delete_bucketlist(self):
        print('=> delete bucket list')
        response = self.app.delete('/api/v1/bucketlists/3', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist_that_does_not_exist(self):
        print('=> delete bucket list')
        response = self.app.delete('/api/v1/bucketlists/300', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 500)

    def test_get_all_bucket_list_item(self):
        print('=> get bucket list item')
        response = self.app.get('/api/v1/bucketlists/items/1', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_get_bucket_list_item(self):
        print('=> get bucket list item by id')
        response = self.app.get('/api/v1/bucketlists/items/1', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(response.data)
        item = resp_data['bucketlist_item'][0]
        self.assertIsNotNone(item)
        self.assertEqual(response.status_code, 200)

    def create_bucketlist_item(self):
        print('=> create bucket list item')
        data = {
            "item_name": "test_bucketlist_item",
            "description": "This is a test bucket list item"
        }
        json_data = json.dumps(data)
        response = self.app.post('/api/v1/bucketlists/1/items', data=json_data, headers={'TOKEN': self.data['TOKEN']})

        resp_data = json.loads(response.data)
        item = resp_data['bucketlist_item'][0]
        self.assertGreater(item['item_id'], 1)
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist_item(self):
        print('=> update item')
        data = {
            "name": 'new_updated_name',
            "done": 'True',
            "description": 'This is a test update call'
        }

        json_data = json.dumps(data)
        response = self.app.put('/api/v1/bucketlists/update-item/5', data=json_data,
                                headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist_item_that_does_not_exist(self):
        print('=> update item')
        data = {
            "name": 'new_updated_name',
            "done": 'False',
            "description": 'This is a test update call'
        }

        json_data = json.dumps(data)
        response = self.app.put('/api/v1/bucketlists/update-item/200', data=json_data,
                                headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 500)

    def test_delete_bucket_list_item(self):
        print('=> delete bucket list item')
        response = self.app.delete('/api/v1/bucketlists/items/6', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_token_api_authenticate(self):
        print('=> test api authenticate')
        response = self.app.get('/auth/authenticate/', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_api_authenticate(self):
        print('=> test fail api authenticate')
        response = self.app.get('/auth/authenticate/', headers={'TOKEN': 'Invalid_Token'})
        self.assertEqual(response.status_code, 401)

    def test_api_search(self):
        print('=> test search functionality')
        response = self.app.get('/api/v1/search/Liyai_list', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)

    def test_api_search_invalid_token(self):
        print('=> test with invalid token')
        response = self.app.get('/api/v1/search/Liyai_list', headers={'TOKEN': 'Invalid_Token'})
        self.assertEqual(response.status_code, 401)

    def test_api_search_object_that_dooes_not_exist(self):
        print('=> test fail search functionality')
        response = self.app.get('/api/v1/search/xsas', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 404)
