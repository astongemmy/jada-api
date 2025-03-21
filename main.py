from werkzeug.middleware.dispatcher import DispatcherMiddleware
from middlewares import create_service_middleware
from utils.logger import setup_app_logger
from werkzeug.wsgi import peek_path_info
from werkzeug.serving import run_simple
from flask import Flask
import logging


# Setup app's logger levels for different environments
setup_app_logger()


# Import available apps
from apis.main import app as apis


apps = [apis]


for app in apps:
  create_service_middleware(app)


class AppDispatcher(DispatcherMiddleware):
  def __call__(self, environ, start_response):
    script = environ.get('PATH_INFO', '')
    prefix = peek_path_info(environ)
    app: Flask = self.mounts.get(f'/{prefix}', self.app)
    logging.info(f'The {app.import_name} app is responding to request url - {script} \n\n\n\n')
    return app(environ, start_response)


app = AppDispatcher('/', {
  '/api': apis
})


if __name__ == '__main__':
  run_simple(
    reloader_type='stat',
    hostname='0.0.0.0',
    use_reloader=True,
    use_debugger=True,
    application=app,
    use_evalax=True,
    port=9000
  )