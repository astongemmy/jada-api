from utils.common import IS_DEVELOPMENT, get_env_variable
import os

# Database variables
db_connection_string = get_env_variable('DATABASE_CONNECTION_STRING')
database_name = get_env_variable('DATABASE_NAME')
database_path = 'postgresql://{}/{}'.format(
  db_connection_string,
  database_name
)

# App config
config = {
  'SQLALCHEMY_DATABASE_URI': database_path,
  'SQLALCHEMY_TRACK_MODIFICATIONS': False,
  'FLASK_DEBUG': IS_DEVELOPMENT
}

# CORS variable
cors_origin = os.getenv('CORS_ORIGIN').split()