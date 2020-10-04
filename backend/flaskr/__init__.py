import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10 

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)


  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  def paging_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    return (questions[start:end])

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()

    paged_questions = paging_questions(request, questions)
    if len(paged_questions) == 0 :
      abort(404)
    return jsonify({
      'success': True,
      'questions': paging_questions(request, questions),
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories}
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter_by(id=question_id).one_or_none()
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
        abort(404)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      JSON_body = request.get_json()
      question = JSON_body.get('question')
      answer = JSON_body.get('answer')
      difficulty = JSON_body.get('difficulty')
      category = JSON_body.get('category')
      question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      question.insert()

      return jsonify({
        'success': True,
        'question_id': question.id
      })

    except:
      abort(422)
    





  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question(): 
    try:  
      JSON_body = request.get_json()
      searchTerm = JSON_body.get('searchTerm') 
      questions = Question.query.filter(Question.question.ilike('%'+searchTerm+'%')).all()
      return jsonify({
        'success': True,
        'questions': paging_questions(request, questions),
        'total_questions': len(questions)
      })

    except:

      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def retrieve_questions_category(category_id):
    questions = Question.query.order_by(Question.id).filter_by(category=category_id).all()
    categories = Category.query.order_by(Category.id).all()


    return jsonify({
      'success': True,
      'questions': paging_questions(request, questions),
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': category_id
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    try:
      next_question = None
      JSON_body = request.get_json()
      previous_questions = JSON_body.get('previous_questions')
      quiz_category = JSON_body.get('quiz_category')

      # if there's a category search for questions in that categoriy
      if quiz_category.get('type') == 'click':
        questions = Question.query.all()
      else:
        questions = Question.query.filter_by(category=int(quiz_category.get('id'))).all()
 
      for question in questions:
        # if the question doesn't exists in the previous_questions send it, else skip it
        if question.id not in previous_questions:
          next_question = question
          break


      # if the loop is done and we didn't find any question
      if next_question is None:
        return jsonify({
        'Success': True,
        'question': False
        })


      return jsonify({
        'Success': True,
        'question': next_question.format()
      })
    except:
      abort(422)


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Un-processable Entity"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500
  
  return app

    