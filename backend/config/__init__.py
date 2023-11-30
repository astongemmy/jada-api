import os

# Database variables
db_connection_string = os.getenv('DATABASE_CONNECTION_STRING')
database_name = os.getenv('DATABASE_NAME')
database_path = 'postgresql://{}/{}'.format(
  db_connection_string,
  database_name
)

# App config
config = {
  'SQLALCHEMY_DATABASE_URI': database_path,
  'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}

# CORS variable
cors_origin = os.getenv('CORS_ORIGIN').split()