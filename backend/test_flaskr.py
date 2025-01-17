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
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'test',
            'answer': 'test',
            'difficulty': 2,
            'category': 2
        }
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
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_getting_categories(self):
        res = self.client().get('/categories')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_getting_questions_page_1(self):
        res = self.client().get('/questions?page=1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_getting_questions_page_99(self):
        res = self.client().get('/questions?page=99')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_getting_not_existing_page(self):
        res = self.client().get('/blahblahblah')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_question_non_existing(self):
        res = self.client().delete('/questions/999')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # number 5 needs to be changed to an existing question id
    def test_delete_question(self):
        res = self.client().delete('/questions/5')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_create_question_missing_json(self):
        res = self.client().post('/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={"searchTerm": "taj"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)

    def test_search_questions_no_json(self):
        res = self.client().post('/questions/search')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_questions_in_category(self):
        res = self.client().get('/categories/1/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], '1')

    def test_search_questions_in_category_non_existing(self):
        res = self.client().get('/categories/99/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        res = self.client().post('/quizzes',
                                 json={"quiz_category": {"type": "sports",
                                       "id": "6"}, "previous_questions": [10]})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
