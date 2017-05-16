import os


class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ['BUCKETLIST_SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['BUCKETLIST_SECRET_KEY']


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_BUCKETLIST_SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['BUCKETLIST_SECRET_KEY']


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
