"""
File      : test_views.py
Date      : April, 2017
Author    : eugene liyai
Desc      : api test file
"""

# ============================================================================
# necessary imports
# ============================================================================
import os

from unittest import TestCase

from bucketlist.controllers.database_controller import DatabaseController


class InitDBTest(TestCase):

    def setUp(self):
        test_database = os.environ['TEST_BUCKETLIST_SQLALCHEMY_DATABASE_URI']
        self.TEST_DATA_CONTROLLER = DatabaseController(test_database)

    def test_initialise_database(self):
        initialized = self.TEST_DATA_CONTROLLER.initialize_database()
        self.assertEqual(initialized, 'Database Initialized')
        dropped = self.TEST_DATA_CONTROLLER.drop_tables()
        self.assertEqual(dropped, 'Database Dropped')
