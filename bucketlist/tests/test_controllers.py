"""
File      : test_controllers.py
Date      : April, 2017
Author    : eugene liyai
Desc      : models test file
"""

# ============================================================================
# necessary imports
# ============================================================================
from unittest import TestCase

from bucketlist.app import app
from bucketlist.controllers import *


class ControllersTest(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        print('Tearing down after test')

    def test_create_user(self):
        request = self.app.post('/')