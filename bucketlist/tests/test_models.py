"""
File      : test_models.py
Date      : April, 2017
Author    : eugene liyai
Desc      : models test file
"""

# ============================================================================
# necessary imports
# ============================================================================
from unittest import TestCase

from bucketlist.models.bucketlist import Bucketlist
from bucketlist.models.bucketlist_items import BucketlistItems
from bucketlist.models.users import Users


class ModelsTest(TestCase):

    def setUp(self):
        self.user = Users()
        self.bucketlist_one = Bucketlist()
        self.bucketlist_two = Bucketlist()
        self.bucket_items_one = BucketlistItems()
        self.bucket_items_two = BucketlistItems()
        self.bucket_items_three = BucketlistItems()

    def test_created_user(self):
        self.assertEqual(self.user.username, 'Paul')

    def test_created_bucketlist(self):
        self.assertEqual(self.bucketlist.bucketlist_name, 'pauls list')

    def test_get_all_created_bucketlist(self):
        self.assertGreater(Bucketlist.query.filter_by(self.user.user_id), 1)

    def test_check_user_password(self):
        self.assertEqual(self.user.hash_password, 'password')

    def test_get_by_username(self):
        self.assertEqual(Users.get_by_username('paul').username, 'paul')

    def test_get_by_user_id(self):
        self.assertEqual(Users.get_by_user_id(1).user_id, 1)

    def test_set_user_password(self):
        self.user.password('password2')
        self.assertTrue(self.user.check_user_password('password2'))

    def test_get_by_bucketlist_id(self):
        self.assertIsNotNone(Bucketlist.get_by_bucketlist_id(1))

    def test_return_all_bucketlist(self):
        self.assertIsNotNone(Bucketlist.return_all_bucketlist())

    def test_get_by_item_id(self):
        self.assertIsNotNone(BucketlistItems.get_by_item_id(1))

    def test_return_all_items(self):
        self.assertIsNotNone(BucketlistItems.return_all())