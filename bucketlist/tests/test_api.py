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


class ViewsTest(TestCase):

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

    def test_get_all_bucketlist(self):
        print('=> Test get all bucket lists')
        request = self.app.get('/api/v1/bucketlists/', headers={'TOKEN': self.data['TOKEN']})
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
        request = self.app.get('/api/v1/bucketlists/items', headers={'TOKEN': self.data['TOKEN']})
        resp_data = json.loads(request.data)
        item = resp_data['bucketlist_item'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(item)

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

    def test_delete_user(self):
        print('=> delete user')
        response = self.app.delete('/api/v1/delete_user/3', headers={'TOKEN': self.data['TOKEN']})
        self.assertEqual(response.status_code, 200)
