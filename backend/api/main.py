from flask_sqlalchemy import SQLAlchemy
from config import config, cors_origin
from api.user import router as user
from flask_cors import CORS
from flask import Flask

db = SQLAlchemy()

# Create flask app
app = Flask('API')
  
# Update app's configuration
app.config.update(config)

# CORS setup
CORS(app=app, origins=cors_origin, supports_credentials=True)

# Register routes
app.register_blueprint(user.app, url_prefix='/api/v1/user')

# Setup database
db.app = app
db.init_app(app)
db.create_all()
  
# Access control setup
@app.after_request
def after_request(response):
  response.headers.add(
    'Access-Control-Allow-Headers',
    'Content-Type,Authentication,True'
  )
    
  response.headers.add(
    'Access-Control-Allow-Methods',
    'GET,PUT,POST,DELETE,OPTIONS'
  )

  return response


# Error handlers for all expected errors
@app.errorhandler(400)
def bad_request(error):
  return {
    'message': 'Bad request',
    'success': False,
    'error': 400
  }, 400


@app.errorhandler(401)
def unauthorized(error):
  return {
    'message': 'Unauthorized',
    'success': False,
    'error': 401
  }, 401


@app.errorhandler(403)
def forbidden(error):
  return {
    'message': 'Forbidden',
    'success': False,
    'error': 403
  }, 403


@app.errorhandler(404)
def not_found(error):
  return {
    'message': 'Resource not found',
    'success': False,
    'error': 404
  }, 404


@app.errorhandler(422)
def unprocessable(error):
  return {
    'message': 'Unprocessable Entity',
    'success': False,
    'error': 422
  }, 422


@app.errorhandler(405)
def not_found(error):
  return {
    'message': 'Method not allowed',
    'success': False,
    'error': 405
  },  405


@app.errorhandler(500)
def server_error(error):
  return {
    'message': 'Server error',
    'success': False,
    'error': 500
  }, 500