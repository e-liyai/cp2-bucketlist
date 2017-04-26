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

    def test_encoded_data_is_string(self):
        self.assertIsInstance(self.encoded_return, str)

    def test_decode_token(self):
        id_return = decode_auth_token(self.encoded_return)
        self.assertEqual(id_return['decode_data'], 10)

    def test_create_token_with_exception(self):
        encoded_fault = encode_auth_token(id)
        self.assertIsInstance(encoded_fault, Exception)

    def test_invalid_token(self):
        id_return = decode_auth_token('invalid_string')
        self.assertEqual(id_return['decode_data'], 'Invalid token. Please log in again.')
