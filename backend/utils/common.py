import os

environment = os.environ['FLASK_ENV']

IS_DEVELOPMENT = environment == 'development'
IS_PRODUCTION = environment == 'production'
IS_STAGING = environment == 'staging'

def get_env_variable(key):
  environment_key_extensions = {
    'development': '_DEVELOPMENT',
    'staging': '_STAGING',
    'local': '_LOCAL',
    'production': ''
  }

  env_key = key + environment_key_extensions[environment]
  # Since not all variables are different for different environments,
  # return the default if an environment specific isn't available.
  return os.getenv(env_key) or os.getenv(key)