import os
from unicodedata import category
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
        
        self.database_path = 'postgresql://rayan:1234@{}/{}'.format('localhost:5432', self.database_name)
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
        """Test _____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(len(data["categories"]),0)
        self.assertEqual(res.status_code, 200)

    # def test_get_all_categories(self):
    #     """Test _____________ """
    #     res = self.client().get('/categories?get=test')

    #     self.assertEqual(res.status_code, 404)

    def test_get_all_questions_pagination(self):
        """Test _____________ """
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"],True)

    def test_404_get_all_questions_pagination(self):
        """Test _____________ """
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_a_question(self):
        """Test _____________ """
        res = self.client().delete('/questions/8')
        question = Question.query.filter(Question.id == 8).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["success"], True)
        self.assertTrue(res.json["question_id"])
        self.assertEqual(question, None)

    def test_422_if_question_doesnt_exist(self):
        """Test _____________ """
        res = self.client().delete('/questions/10000')
        question = Question.query.filter(Question.id == 10000).one_or_none()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json["success"], False)
        # self.assertTrue(res.json["question_id"])
        self.assertEqual(question, None)

    def test_post_questions(self):
        """Test _____________ """
        res = self.client().post('/questions', json={
           "questions":"last worldcup winner","answer":"France","category":1,"difficulty":1
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_404_post_questions(self):
        """Test _____________ """
        res = self.client().post('/questions', json={
           "answer":"France","category":1,"difficulty":1
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_get_questions_by_search(self):
        """Test _____________ """
        res = self.client().post('/questions/search', json={
           "searchTerm":"a"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_404_questions_by_search(self):
        """Test _____________ """
        res = self.client().post('/questions/search', json={
           "searchTerm":"cccccccc"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_get_questions_by_category(self):
        """Test _____________ """
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code,200)
        self.assertTrue(res.json["questions"])

    def test_404_questions_by_category(self):
        """Test _____________ """
        res = self.client().get('/categories/66/questions')
        self.assertEqual(res.status_code,404)
        self.assertFalse(res.json["success"])       
    

    def test_get_quizz(self):
        """Test _____________ """
        res = self.client().post('/quizzes', json={"previous_questions":[],"quiz_category":{"type":"social","id":1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data["question"])
        self.assertTrue(data["success"])


    def test_404_quizz_not_found(self):
        """Test _____________ """
        res = self.client().post('/quizzes', json={"previous_questions":[],"quiz_category":""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertFalse(data["success"])       
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()