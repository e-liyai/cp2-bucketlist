"""
    File      : manage.py
    Date      : February, 2017
    Author    : eugene liyai
    Desc      : Runs the application and initates the database
"""

# ============================================================================
# necessary imports
# ============================================================================
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from bucketlist.app import app
from bucketlist.init_test_db import *

migrate = Migrate(app)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    init_bucketlist_database()


@manager.command
def populatedb():
    fill_database()
    print('Database populated')


@manager.command
def dropdb():
    drop_database_tables()
    print('Dropped the database')


@manager.command
def init_test_db():
    initialize_test_database()


@manager.command
def drop_test_db():
    print('Test database dropped')
    drop_test_database()


if __name__ == '__main__':
    manager.run()
