import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        response = self.client().get('/api/v1/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'], True)

    def test_get_paginated_questions(self):
        response = self.client().get('/api/v1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['current_category'])

    def test_get_paginated_questions_invalid_page(self):
        response = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question_success(self):
        question_id = 20
        response = self.client().delete(f'/api/v1/questions/{question_id}')
        data = json.loads(response.data)

        question = Question.query.filter_by(id=question_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_delete_question_not_found(self):
        question_id = 1000
        response = self.client().delete(f'/api/v1/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_create_new_question_success(self):
        payload = {
            'question': 'Who is the chicken',
            'answer': 'We am',
            'category': 4,
            'difficulty': 1
        }
        response = self.client().post(f'/api/v1/questions', json=payload)
        data = json.loads(response.data)

        question = Question.query.filter(Question.question.ilike(r'%Who is the chicken%')).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(question)
        self.assertEqual(payload['question'], question.question)

    def test_create_new_question_not_allowed(self):
        payload = {
            'questions': 'What is 1000',
            'answer': 1000,
            'category': 4,
            'difficulty': 1
        }
        response = self.client().post(f'/api/v1/questions/1', json=payload)
        data = json.loads(response.data)

        question = Question.query.filter(Question.question.ilike('%What is 1000%')).one_or_none()

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)

    def test_search_for_questions_successful(self):
        payload = {'searchTerm': 'title'}

        response = self.client().post(f'/api/v1/questions', json=payload)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_question_by_category_success(self):
        response = self.client().get('/api/v1/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    def test_get_question_by_category_not_found(self):
        response = self.client().get('/api/v1/categories/10000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()