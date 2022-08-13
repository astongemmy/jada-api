import json
from sqlalchemy import and_, or_, func
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type = int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_page_questions = questions[start:end]

    return current_page_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origin='*', supports_credentials=True)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authentication,True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods = ['GET'])
    def get_all_categories():
        categories = Category.query.all()

        if len(categories) == 0: abort(404)

        responseDict = {
            'success': True,
            'message': 'Categories returned successfully.',
            'categories': {}
        }

        for category in categories:
            responseDict['categories'][category.id] = category.type
        
        return jsonify(responseDict)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods = ['GET'])
    def get_all_questions():
        questions = Question.query.order_by(Question.id).all()
        
        current_page_questions = paginate_questions(request, questions)
        
        if len(current_page_questions) == 0: abort(404)

        responseDict = {
            'success': True,
            'message': 'Questions returned successfully.',
            'questions': [],
            'total_questions': 0,
            'current_category': None,
            'categories': {}
        }

        categories = Category.query.all()

        if len(categories) > 0:
            for category in categories:
                responseDict['categories'][category.id] = category.type

        responseDict['questions'] = current_page_questions
        responseDict['total_questions'] = len(questions)
        responseDict['current_category'] = ''
        
        return jsonify(responseDict)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods = ['DELETE'])
    def delete_question(question_id):        
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None: abort(404)

            question.delete()

            responseDict = {
                'success': True,
                'message': 'Question deleted successfully.',
                'deleted': question_id
            }

            return jsonify(responseDict)
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            question = Question(
                question = question,
                answer = answer,
                category = category,
                difficulty = difficulty
            )

            question.insert()

            return jsonify({
                'success': True,
                'message': 'Question created successfully.',
                **body
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods = ['POST'])
    def search_question():
        body = request.get_json()

        search = body.get("searchTerm", None)

        try:
            questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            ).all()
            
            current_page_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'message': 'Search questions returned successfully.',
                'questions': current_page_questions,
                'total_questions': len(questions),
                'current_category': ''
            })
        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
    def get_category_questions(category_id):
        try:
            category_questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in category_questions]

            responseDict = {
                'success': True,
                'message': 'Category questions returned successfully.',
                'questions': formatted_questions,
                'total_questions': len(category_questions),
                'current_category': None
            }

            return jsonify(responseDict)
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods = ['POST'])
    def play_quiz():
        body = request.get_json()

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        
        responseDict = {
            'success': True,
            'message': 'Quiz question returned successfully.',
        }

        try:
            quiz_question = Question.query.filter(
                and_(
                    Question.category == quiz_category['id'] if quiz_category['id'] else Question.category > 0,
                    ~Question.id.in_(previous_questions)
                )
            ).order_by(func.random()).first()
            
            if quiz_question: responseDict['question'] = quiz_question.format()

            return jsonify(responseDict)
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "server error"}),
            500,
        )

    return app