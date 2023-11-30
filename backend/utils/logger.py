from utils.env import IS_DEVELOPMENT, IS_PRODUCTION
from werkzeug.exceptions import HTTPException
from flask import Flask, Response, g
import traceback
import logging

def setup_app_logger():
  # try:
  #   if not IS_DEVELOPMENT:
  #     print('Production logger will be attached here!')
  # except RuntimeError:
    # If debugger is available, an error is raised
    # pass

  # if not IS_DEVELOPMENT:
    # import cloud logger here
 
  if IS_DEVELOPMENT:
    logging.basicConfig(level=logging.DEBUG)

def log_main_request(response: Response) -> Response:
  if IS_DEVELOPMENT:
    return response

  log_level = g.get('log_level', 0)
  if log_level < logging.WARNING:
    return response

  status = getattr(response, 'status_code', 500)

  request_logger = logging.getLogger('request')
  request_logger.log(log_level, '', extra={'status': status})

  if g.get('error_msg', None):
    error_logger = logging.getLogger('errorReporter')
    error_logger.log(log_level, '', extra={'status': status})

  return response

def handle_exception(exception):
  if IS_DEVELOPMENT:
    raise exception
  
  logging.exception(exception)
  message = traceback.format_exc()
  g.error_msg = message

  if isinstance(exception, HTTPException):
    return exception

  message = str(exception) if IS_DEVELOPMENT else 'Internal Server Error'
  return message, 500

class FlaskLogger():
  def __init__(self, app: Flask):
    self.handle_exception(app)
    # self.instrumentation(app)
    self.after_request(app)

  def handle_exception(self, app: Flask):
    app.errorhandler(Exception)(handle_exception)

  # def instrumentation(self, app: Flask):
  #   app.instrument_app(app)
  
  def after_request(self, app: Flask):
    app.after_request(log_main_request)