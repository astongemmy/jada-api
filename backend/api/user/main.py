from flask_restx import Api
from flask import Blueprint

app = Blueprint('user', __name__)

auth = {
  'apiKey': {
    'name': 'X-ROWAPP-AUTH',
    'type': 'apiKey',
    'in': 'header',
  }
}

router = Api(
  app,
  auhorization=auth,
  security='apiKey',
  doc='/api-docs'
)
