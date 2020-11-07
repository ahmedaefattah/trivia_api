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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.question = {
        'question': 'Which country won the  soccer World Cup in  2006',
        'answer': 'Italy',
        'category': 6,
        'difficulty': 3
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
    Write at least one test for each test for successful operation and for expected errors.
    """




    # Test Get '/questions' end point for valid request. 
    def test_get_paginated_questions(self):
        res  = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test Get '/questions' end point for invalid request. 
    def test_404_sent_requesting_beynod_valid_page(self):
        res  = self.client().get('/quesions/?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    
    # Test  Create question '/questions' end point.
    def test_create_new_question(self):
        res  = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    

    #Test create question by invaild request.
    def  test_405_if_question_creation_not_allowed(self):
        res  = self.client().post('/questions/50', json= self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Method not allowed')

    
    # Test Delete question '/questions/<int:question_id>' end point.
    def test_delete_question(self):
        res  = self.client().delete('/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
    
    

    # Test Delete question for a  question id not exist.
    def test_422_question_does_not_exist(self):
        res  = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    # Test Search end point for vaild search term .
    def test_get_question_search_with_results(self):
        res  = self.client().post('/questions/search', json={'searchTerm': 'Egyptians'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    # Test Search end point for invaild search term .
    def test_get_book_search_without_results(self):
        res  = self.client().post('/questions/search', json={'searchTerm': 'notfound'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    #Test POST '/categories/<int:category_id>/questions' end point for vaild category ID.
    def test_get_questions_based_on_category(self):
        res  = self.client().post('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_category'])

    #Test POST '/categories/<int:category_id>/questions' end point for invaild category ID.
    def test_404_sent_requesting_beynod_valid_category_id(self):
        res  = self.client().post('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test Get '/categories' end point for valid request. 
    def test_get_all_categories(self):
        res  = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Test Get '/categories' end point for invalid request method. 
    def  test_405_get_all_categories_method_not_allowed(self):
        res  = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Method not allowed')

    # Test POST '/quizzes' end point for vaild request. 
    def test_play_quiz(self):

        res = self.client().post('/quizzes', json={'previous_questions': [],'quiz_category': {'type': 'Sport', 'id': 6}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

     # Test POST '/quizzes' end point for invaild request. 
    def test_404_play_quiz(self):

        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()