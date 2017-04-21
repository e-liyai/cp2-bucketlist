"""
File      : test_views.py
Date      : April, 2017
Author    : eugene liyai
Desc      : api test file
"""

# ============================================================================
# necessary imports
# ============================================================================
import requests
import json

from unittest import TestCase

from bucketlist.app import app


class ViewsTest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        print('Tearing down after test')

    def test_get_all_bucketlist(self):
        request = self.app.get('/api/v1/bucketlists/')
        self.assertEqual(request.status_code, 200)

    def test_get_bucketlist_by_id(self):
        request = self.app.get('/api/v1/bucketlists/1')
        resp_data = json.loads(request.data)
        bucket_list = resp_data['bucketlists'][0]
        self.assertEqual(request.status_code, 200)
        self.assertIsNotNone(bucket_list)


