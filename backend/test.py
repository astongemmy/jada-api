from dotenv import load_dotenv
load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from api.main import app
import unittest
import os

from tests.api.api import *

class TriviaTestCase(unittest.TestCase):
  def setUp(self):
    """Define test variables and initialize app."""
    self.app = app
    self.client = self.app.test_client
    self.database_name = os.getenv('TEST_DATABASE_NAME')
    self.db_connection_string = os.getenv('DATABASE_CONNECTION_STRING')
    self.database_path = "postgresql://{}/{}".format(self.db_connection_string, self.database_name)
    
    self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
    self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
      
    self.search_term = "What is the duration of Udacity Nanodegree program?"
    self.new_question = {
      "question": "What is the duration of Udacity Nanodegree program?",
      "answer": "3 months",
      "difficulty": 4,
      "category": 1
    }
    
    self.quiz = {
      'previous_questions': [20, 22],
      'quiz_category': {
        'type': 'Science',
        'id': 1
      }
    }
    
  def tearDown(self):
    """Executed after each test"""
    pass

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()