"""
File      : init_test_db.py
Date      : April, 2017
Author    : eugene liyai
Desc      : initialize test database
"""

# ============================================================================
# necessary imports
# ============================================================================
import os

from bucketlist.controllers.database_controller import DatabaseController

# development database
db_engine = os.environ['BUCKETLIST_SQLALCHEMY_DATABASE_URI']
DATA_CONTROLLER = DatabaseController(db_engine)

# test database
test_database = os.environ['TEST_BUCKETLIST_SQLALCHEMY_DATABASE_URI']
TEST_DATA_CONTROLLER = DatabaseController(test_database)


def initialize_test_database():
    TEST_DATA_CONTROLLER.initialize_database()


def drop_test_database():
    TEST_DATA_CONTROLLER.drop_tables()


def init_bucketlist_database():
    DATA_CONTROLLER.initialize_database()


def fill_database():
    DATA_CONTROLLER.populate_database()


def drop_database_tables():
    DATA_CONTROLLER.drop_tables()