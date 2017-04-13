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
from bucketlist.apis.api_routes import *

migrate = Migrate(app)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    init_bucketlist_database()


@manager.command
def populatedb():
    fill_database()


@manager.command
def dropdb():
    drop_database_tables()
    print('Dropped the database')

if __name__ == '__main__':
    manager.run()
