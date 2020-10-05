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
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paging_questions(request, questions):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in questions]
        return (questions[start:end])

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()

        if (len(categories) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'categories': {category.id: category.type
                           for category in categories}
        })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()

            paged_questions = paging_questions(request, questions)

            if len(paged_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': paging_questions(request, questions),
                'total_questions': len(questions),
                'categories': {category.id: category.type
                               for category in categories}
            })
        except Exception:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            JSON_body = request.get_json()
            question = JSON_body.get('question')
            answer = JSON_body.get('answer')
            difficulty = JSON_body.get('difficulty')
            category = JSON_body.get('category')
            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()

            return jsonify({
                'success': True,
                'question_id': question.id
            })

        except Exception:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            JSON_body = request.get_json()
            searchTerm = JSON_body.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(
                '%'+searchTerm+'%')).all()
            return jsonify({
                'success': True,
                'questions': paging_questions(request, questions),
                'total_questions': len(questions)
            })

        except Exception:
            abort(422)

    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def retrieve_questions_category(category_id):
        try:
            questions = Question.query.order_by(Question.id).filter_by(
                category=category_id).all()

            if len(questions) == 0:
                abort(404)

            categories = Category.query.order_by(Category.id).all()
            paged_questions = paging_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': paged_questions,
                'total_questions': len(questions),
                'categories': {category.id: category.type
                               for category in categories},
                'current_category': category_id
            })
        except Exception:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        try:
            next_question = None
            JSON_body = request.get_json()
            previous_questions = JSON_body.get('previous_questions')
            quiz_category = JSON_body.get('quiz_category')

            # if there's a category search for questions in that categories
            if quiz_category.get('type') == 'click':
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                  category=int(quiz_category.get('id'))).all()
            for question in questions:
                # if the question doesn't exists in the previous_questions
                #  return it, else skip it.
                if question.id not in previous_questions:
                    next_question = question
                    break

            # if the loop is done and we didn't find any question
            if next_question is None:
                return jsonify({'Success': True, 'question': False})

            return jsonify({
              'success': True,
              'question': next_question.format()
            })
        except Exception:
            abort(422)

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
