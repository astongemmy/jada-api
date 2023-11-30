from utils.logger import FlaskLogger
from flask_caching import Cache
from config.cache import config
from flask import Flask

def ndb_wsgi_middleware(wsgi_app):
  def middleware(environ, start_response):
    # global_cache = RedisCache(REDISCLIEN)
    # context = ndb.context.get_context(False)

    # if not context:
    #   with client.context(global_cache=global_cache):
    #     return wsgi_app(environ, start_response)
    
    return wsgi_app(environ, start_response)
  
  return middleware

def create_service_middleware(app: Flask):
  app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)
  FlaskLogger(app)
  
  cache = Cache(config=config)
  cache.init_app(app)