from .utils.response import ApiResponse
from flask_sqlalchemy import SQLAlchemy
from config import config, cors_origin
from api.user import router as user
from .utils.app import create_app
from flask_cors import CORS

db = SQLAlchemy()

# Create and get flask app instance
app, handle_user_exception, handle_exception = create_app(name='API', config=config)

# CORS setup
CORS(app=app, origins=cors_origin, supports_credentials=True)

# Register routes
app.register_blueprint(user.app, url_prefix='/api/v1/user')

# Flask_restx has been initialized in Blueprint's import therefore,
# re-assign error handling control from flask_restx to flask
app.handle_user_exception = handle_user_exception
app.handle_exception = handle_exception

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
@app.errorhandler(422)
def unprocessable(error):
  return ApiResponse.unprocessable(data=error.description)

@app.errorhandler(405)
def not_allowed(error):
  return ApiResponse.not_allowed(data=error.description)

@app.errorhandler(404)
def not_found(error):
  return ApiResponse.not_found(data=error.description)

@app.errorhandler(400)
def bad_request(error):
  return ApiResponse.bad_request(data=error.description)

@app.errorhandler(401)
def unauthorized(error):
  return ApiResponse.unauthorized(data=error.description)

@app.errorhandler(403)
def forbidden(error):
  return ApiResponse.forbidden(data=error.description)

@app.errorhandler(500)
def server_error(error):
  return ApiResponse.server_error(data=error.description)