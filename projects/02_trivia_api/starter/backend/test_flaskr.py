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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
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
    def test_get_paginated_questions(self):
        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_delete_question(self):
        resp = self.client().delete('/questions/34')
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_nonexisting_question(self):
        resp = self.client().delete('/questions/1000')
        data = json.loads(resp.data)

        self.assertNotEqual(resp.status_code, 200)

    def test_get_categories(self):
        resp = self.client().get('/categories')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz(self):
        quiz_category = 'Science'
        resp = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {
                'type': quiz_category,
                'id': 0}
                })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_play_quiz(self):
        quiz_category = 'Nothing'
        resp = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {
                'type': quiz_category,
                'id': 5}
                })
        data = json.loads(resp.data)

        self.assertNotEqual(data['success'], True)

    def test_search_questions(self):
        search_term = "title"
        resp = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(resp.data)
        #print(f'title search response: {data}')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_search_questions(self):
        search_term = "girls"
        resp = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(resp.data)

        self.assertEqual(data['success'], False)

    def test_get_category_questions(self):
        #category_id = 1
        resp = self.client().get('/categories/1/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_get_category_questions(self):
        #category_id = 100
        resp = self.client().get('/categories/100/questions')
        data = json.loads(resp.data)

        self.assertNotEqual(resp.status_code, 200)

    def test_add_question(self):
        resp = self.client().post('/questions', json={
            'question': 'Test add question',
            'answer': 'This is a test',
            'category': 1,
            'difficulty': 3
        })
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_add_question(self):
        resp = self.client().post('/questions', json={
            'question': 'Test fail add question',
            'answer': 'This is a test',
            'category': 10,
            'difficulty': 5
        })
        data = json.loads(resp.data)

        self.assertNotEqual(resp.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()