
from models import setup_db, Question, Category
from flask_sqlalchemy import SQLAlchemy
from unicodedata import category
from app import create_app
import unittest
import json
import os


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('TEST_DATABASE_NAME')
        self.db_connection_string = os.getenv('DATABASE_CONNECTION_STRING')
        self.database_path = "postgresql://{}/{}".format(self.db_connection_string, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.searchTerm = {
            "searchTerm": "What is the duration of Udacity Nanodegree program?"
        }

        self.new_question = {
            "question": "What is the duration of Udacity Nanodegree program?",
            "answer": "3 months",
            "category": 1,
            "difficulty": 4
        }

        self.quiz = {
            'previous_questions': [20, 22],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["answer"])
        self.assertTrue(data["category"])
        self.assertTrue(data["difficulty"])

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_category_questions(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_question(self):
        res = self.client().post("/questions/search", json=self.searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_play_quiz(self):
        res = self.client().post("/quizzes", json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]['id'] not in self.quiz['previous_questions'])

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]) <= 10)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_404_if_question_not_found(self):
        res = self.client().get("/questions?page=200")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/200", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 2)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()