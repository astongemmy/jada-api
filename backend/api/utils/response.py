class ApiResponse():
  # SECCESS RESPONSES
  def created(message='Resource created successful', data={}):
    return {
      'message': message,
      'success': True,
      'data': data
    }, 201
  
  def ok(message='Request successful', data={}):
    return {
      'message': message,
      'success': True,
      'data': data
    }, 200
  

  # HTTP EXCEPTIONS
  def server_error(message='Internal server error', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 500

  def unprocessable(message='Unprocessable entity', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 422
  
  def not_allowed(message='Method not allowed', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 405

  def bad_request(message='Resource not found', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': 'Bad request',
      'success': False,
      'data': data
    }, 400
  
  def not_found(message='Resource not found', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 404
  
  def unauthorized(message='Unauthorized', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 401

  def forbidden(message='Forbidden', data={}):
    data = data if type(data) in [list, dict] else {}
    return {
      'message': message,
      'success': False,
      'data': data
    }, 403