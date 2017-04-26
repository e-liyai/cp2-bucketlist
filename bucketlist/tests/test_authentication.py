"""
File      : test_authentication.py
Date      : April, 2017
Author    : eugene liyai
Desc      : token test file
"""

# ============================================================================
# necessary imports
# ============================================================================
import json

from unittest import TestCase

from bucketlist.controllers.authentication_controller import encode_auth_token, decode_auth_token


class TokenAuthentcationTest(TestCase):

    def setUp(self):
        self.encoded_return = encode_auth_token(10)

    def test_encode_data(self):
        self.assertIsNotNone(self.encoded_return)

    def test_decode_token(self):
        id_return = decode_auth_token(self.encoded_return)
        self.assertEqual(id_return['decode_data'], 10)
