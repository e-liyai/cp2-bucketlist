"""
File      : app.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Runs the flask api application
"""

# ============================================================================
# necessary imports
# ============================================================================
from flask import Flask
from flask_login import LoginManager

from bucketlist.config import app_config

# Create flask application
app = Flask(__name__, instance_path='/instance')

app.config['SECRET_KEY'] = 'Bucketlist api application, keep your list updated'
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)


from bucketlist.apis.api_routes import initialize_api_routes
initialize_api_routes(app)

