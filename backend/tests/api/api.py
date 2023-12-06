from models.question import Question
from test import TriviaTestCase
import json

class ApiTestCase(TriviaTestCase):
    def get_data(self, data):
        data = json.loads(data)
        
        success = data.get('success')
        message = data.get('message')
        data = data.get('data')

        return success, data, message
        
    def test_create_new_question(self):
        res = self.client().post('/api/v1/user/questions', json=self.new_question)
        success, data, _ = self.get_data(res.data)

        self.assertEqual(data, self.new_question)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(success, True)

    def test_get_categories(self):
        res = self.client().get('/api/v1/user/categories')
        success, _, _ = self.get_data(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)

    def test_get_category_questions(self):
        res = self.client().get('/api/v1/user/categories/4/questions')
        success, _, _ = self.get_data(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)

    def test_search_question(self):
        res = self.client().get('/api/v1/user/questions/search?q={self.search_term}')
        success, _, _ = self.get_data(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)

    def test_play_quiz(self):
        res = self.client().post('/api/v1/user/quizzes', json=self.quiz)
        success, data, _ = self.get_data(res.data)

        self.assertTrue(data.get('question')['id'] not in self.quiz.get('previous_questions'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)

    def test_get_paginated_questions(self):
        res = self.client().get('/api/v1/user/questions')
        success, data, _ = self.get_data(res.data)

        self.assertTrue(len(data.get('questions')) <= 10)
        self.assertTrue(data.get('total_questions'))
        self.assertTrue(data.get('categories'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)

    def test_404_if_question_not_found(self):
        res = self.client().get('/api/v1/user/questions/?page=200')
        success, _, message = self.get_data(res.data)

        self.assertEqual(message, 'Resource not found')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(success, False)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/api/v1/user/questions/200', json=self.new_question)
        success, _, message = self.get_data(res.data)

        self.assertEqual(message, 'Method not allowed')
        self.assertEqual(res.status_code, 405)
        self.assertEqual(success, False)

    def test_delete_question(self):
        res = self.client().delete('/api/v1/user/questions/2')
        success, data, _ = self.get_data(res.data)
        
        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(data.get('deleted'), 2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/api/v1/user/questions/1000')
        success, _, message = self.get_data(res.data)

        self.assertEqual(message, 'Question not found')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(success, False)
    
    def test_405_if_question_id_was_not_provided(self):
        res = self.client().delete('/api/v1/user/questions')
        success, _, message = self.get_data(res.data)
        
        self.assertEqual(message, 'Method not allowed')
        self.assertEqual(res.status_code, 405)
        self.assertEqual(success, False)