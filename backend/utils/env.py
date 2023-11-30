import os

IS_DEVELOPMENT = os.environ['FLASK_ENV'] == 'development'
IS_PRODUCTION = os.environ['FLASK_ENV'] == 'production'