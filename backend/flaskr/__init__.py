from crypt import methods
import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from random import choice

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories_request = Category.query.all()
        categories = {}
        # categories = dict([category.format() for category in categories_request])
        for category in categories_request:
            categories[category.id] = category.type

        # print(categories)

        return jsonify({
            "success": True,
            "categories": categories
        })

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
    @app.route("/questions", methods=["GET"])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        selected_questions = Question.query.order_by(Question.id).all()
        questions = [qst.format() for qst in selected_questions]
        current_questions = questions[start:end]

        categories_query = Category.query.all()
        categories = {}
        for category in categories_query:
            categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": categories

        }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
           question_deleted = Question.query.filter(
                Question.id == question_id).one_or_none()
        #    if question_deleted == None:
        #         abort(422)
           Question.delete(question_deleted)
        except Exception as e :
            abort(422)
        return jsonify({
            "success": True,
            "question_id": question_id
        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def post_question():
        try:
            Question.insert(Question(
                request.json["question"], request.json["answer"], request.json["difficulty"], request.json["category"]))
        except:
            abort(500)
        return jsonify({
            "success": True
        })
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        try:
            questions = Question.query.filter(func.lower(Question.question).contains(
                func.lower(request.json['searchTerm']))).all()
            if (questions):
                
                questions_formated = [qst.format() for qst in questions]
            else:
                abort(404)

        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            "questions": questions_formated
        })
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            questions_request = Question.query.join(Category).filter(
                Question.category == category_id).all()

            if questions_request:
                questions = [qst.format() for qst in questions_request]
                return jsonify({
                    'questions': questions
                })
            else:
                abort(404)
        except Exception as e:
            abort(404)
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
    @app.route("/quizzes", methods=["POST"])
    def search_next_question():
        current_category = request.json["quiz_category"]
        previous_questions = request.json["previous_questions"]
        try:
            questions = {}
            qst_id = 2

            if current_category["type"] == "click":
                questions_request = Question.query.all()
            else:
                questions_request = Question.query.join(Category).filter(
                Category.id == current_category["id"]).all()
            if questions_request:
                qst_id = random.randint(0, len(questions_request)-1)
                print(previous_questions)
                randomized = False

                if len(questions_request) == len(previous_questions):
                    abort(404)

                while(not randomized):
                    print(questions_request[qst_id].id)
                    if questions_request[qst_id].id not in previous_questions:
                        randomized = True
                    else:
                        qst_id = random.randint(0, len(questions_request)-1)
                questions = questions_request[qst_id].format()
            else:
                abort(404)
                


        except Exception as e :
                abort(404)            

        return jsonify({
            "success": True,
            "question": questions,
            "previous_questions": previous_questions
        })
    """    

    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

# this one won't be used because we don't have autorisations yet
    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    return app
