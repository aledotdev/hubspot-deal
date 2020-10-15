import os


class BaseSettings(object):
    # Flask settings
    FLASK_SERVER_NAME = 'localhost:{}'.format(int(os.getenv('HBDEAL_SERVER_PORT', 5000)))
    FLASK_DEBUG = bool(os.getenv('HBDEAL_DEBUG', False))  # Do not use debug mode in production
    SECRET_KEY = os.getenv('HBDEAL_SECRET_KEY')

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    # DB Settings
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/hbdeal'
    }

    HB_OAUTH_REDIRECT_URL = os.getenv('HB_OAUTH_REDIRECT_URL')


class ProdSettings(BaseSettings):
    pass


class DevSettings(BaseSettings):
    DEBUG = bool(os.getenv('HBDEAL_DEBUG', True))  # Do not use debug mode in production
    SECRET_KEY = "DEV-SECRET-123456789"
    HB_OAUTH_REDIRECT_URL = os.getenv('HB_OAUTH_REDIRECT_URL', 'https://aledev.net/user/hb-oauth')
    


class TestSettings(BaseSettings):
    DEBUG = False
    TESTING = True
    SECRET_KEY = "TEST-SECRET-123456789"
