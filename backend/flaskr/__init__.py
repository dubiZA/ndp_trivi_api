import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    all_questions = [question.format() for question in selection]
    current_questions = all_questions[start:end]

    return {
        'current_page': page,
        'total_questions': len(all_questions),
        'current_questions': current_questions
    }



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r'/api/v1/*': {'origins': '*'}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET,PATH,POST,DELETE,OPTIONS')
        return response


    # ERROR HANDLERS

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422


    # ROUTES

    @app.route('/api/v1/categories')
    def get_categories():
        ''' Handles requests for categories.

        Accepts get requests for categories and retrieves all categories from the database.

        Returns:
            A JSON response reporting success and all categories as JSON objects or an HTTP
            404 if there are no categories retrieved from the DB.

        Raises:
            An HTTP 422 is returned if the request cannot be successfully processed.
        '''
        try:
            categories = Category.query.order_by(Category.id).all()
        except:
            abort(422)

        if not categories:
            abort(404)

        formatted_categories = {category.id:category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/api/v1/questions')
    def get_questions():
        ''' Handles requests for questions.

        Accepts get requests for questions and retrieves all questions from the database.

        Returns:
            A JSON response reporting success, a list of formatted questions, total questions
            the current page of results and all categories as JSON objects. If the are no
            questions retrieved from the database, an HTTP 404 is returned.

        Raises:
            An HTTP 422 is returned if the request cannot be successfully processed.
        '''
        try:
            all_questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
        except:
            abort(422)

        current_questions = paginate(request, all_questions)

        if len(current_questions['current_questions']) == 0:
            abort(404)

        formatted_categories = {category.id:category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': current_questions['current_questions'],
            'categories': formatted_categories,
            'current_category': 'Placeholder',
            'total_questions': current_questions['total_questions'],
            'current_page': current_questions['current_page']
        })

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        ''' Handles delete requests for questions by ID.

        Accepts delete requests for questions by ID and deletes the specified
        question from the database.

        Returns:
            A JSON response reporting success, the question id for the deleted
            question, a list of formatted questions, total questions the current
            page of results and all categories as JSON objects. If the does not
            exist in the database, an HTTP 404 is returned.

        Raises:
            An HTTP 422 is returned if the request cannot be successfully processed.
        '''
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
        except:
            abort(422)

        if question is None:
                abort(404)

        try:
            question.delete()
            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, all_questions)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions['current_questions'],
                'total_questions': current_questions['total_questions'],
                'current_page': current_questions['current_page']
            })
        except:
            abort(422)

    @app.route('/api/v1/questions', methods=['POST'])
    def create_question():
        ''' Handles post requests for question.

        Accepts post requests for new questions that a users submits to the
        database.

        Returns:
            A JSON response reporting success, a list of formatted questions, total
            questions and the current page of results as JSON objects.

        Raises:
            An HTTP 422 is returned if the new question is unable to be added to the DB
        '''
        if request.get_json().get('searchTerm'):
            search_term = request.get_json().get('searchTerm')
            search_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            if not search_questions:
                abort(404)
            else:
                search_results = paginate(request, search_questions)

                return jsonify({
                    'success': True,
                    'questions': search_results['current_questions'],
                    'total_questions': search_results['total_questions'],
                    'current_page': search_results['current_page']
                })
        else:
            request_body = request.get_json()
            new_question = request_body.get('question', None)
            new_answer = request_body.get('answer', None)
            new_category = int(request_body.get('category', None))
            new_difficulty = int(request_body.get('difficulty', None))

            try:
                new_question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                new_question.insert()

                all_questions = Question.query.order_by(Question.id).all()
                current_questions = paginate(request, all_questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions['current_questions'],
                    'total_questions': current_questions['total_questions'],
                    'current_page': current_questions['current_page']
                })
            except:
                abort(422)

    @app.route('/api/v1/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        ''' Handles get requests for questions by category.

        Accepts get requests for questions by a user selected category.

        Returns:
            A JSON response reporting success, a list of formatted questions, total
            questions, all categories, the user selected current category and the
            current page of results as JSON objects. If the category does not exist
            in the DB or there are no questions for a valid category selection, an
            HTTP 404 is returned.

        Raises:
            An HTTP 422 is returned if the request cannot be successfully processed.
        '''
        selected_category = Category.query.filter_by(id=category_id).one_or_none()

        if selected_category is None:
            abort(404)

        questions = Question.query.filter_by(category=selected_category.id).order_by(Question.id).all()

        if not questions:
            abort(404)

        try:
            current_questions = paginate(request, questions)
            all_categories = Category.query.order_by(Category.id).all()
            formatted_categories = {category.id:category.type for category in all_categories}

            return jsonify({
                'success': True,
                'questions': current_questions['current_questions'],
                'categories': formatted_categories,
                'current_category': selected_category.type,
                'total_questions': current_questions['total_questions'],
                'current_page': current_questions['current_page']
            })
        except:
            abort(422)

    @app.route('/api/v1/quizzes', methods=['POST'])
    def start_quiz():
        ''' Handles post requests for quiz answer submissions.

        Accepts post requests for questions by a user selected category. The
        question is randomly selected and returned to the user for answer.

        Returns:
            A JSON response reporting success, a randomly selected question and the
            remaining number of questions for the category selection as JSON objects.
            If there are no questions, an HTTP 404 is returned.

        Raises:
            An HTTP 422 is returned if the request cannot be successfully processed.
        '''
        request_body = request.get_json()

        selected_category = request_body.get('quiz_category')
        previous_questions = request_body.get('previous_questions')

        try:
            if selected_category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).order_by(Question.id).all()
            else:
                questions = Question.query.filter(Question.category == selected_category['id'], Question.id.notin_(previous_questions)).order_by(Question.id).all()
        except:
            abort(422)

        if not questions:
            abort(404)
        
        available_questions = [question.format() for question in questions]
        random_question = random.choice(available_questions)

        return jsonify({
            'success': True,
            'question': random_question,
            'remaining_questions': len(available_questions)-1
        })


    return app
