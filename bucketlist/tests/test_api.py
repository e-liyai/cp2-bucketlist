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

from unittest import TestCase
from mock import Mock, patch

from bucketlist.apis.login_register_apis import LoginRegister
from bucketlist.apis.bucketlist_apis import BucketlistApis


class ViewsTest(TestCase):

    def setUp(self):
        self.login_register = LoginRegister()
        self.bucketlist_apis = BucketlistApis()

    def test_get_login_url(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.login_register.login())

    def test_post_register_url(self):
        with patch.object(requests, 'post') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.login_register.register())

    def test_list_bucketlists(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.list_bucketlists())

    def test_do_create_bucketlist(self):
        with patch.object(requests, 'post') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.list_bucketlists())

    def test_get_single_bucket_list(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())

    def test_update_bucket_list(self):
        with patch.object(requests, 'put') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())

    def test_delete_single_bucket_list(self):
        with patch.object(requests, 'delete') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())

    def test_create_item_in_bucketlist(self):
        with patch.object(requests, 'post') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())

    def test_update_bucket_listitem(self):
        with patch.object(requests, 'put') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())

    def test_delete_item_in_bucketlist(self):
        with patch.object(requests, 'delete') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            self.assertEqual(200, self.bucketlist_apis.get_single_bucket_list())
