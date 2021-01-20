import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, origins = '*')
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Methods'] = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS']
    response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      data = Category.query.order_by(Category.id).all()
      if data is None:
        abort(404)
      else:
        categories = [item.type for item in data]
        return jsonify({
          'success': True,
          'categories': categories})
    except:
      abort(404)

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
  def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = [question.format() for question in questions[start:end]]
    return current_questions
  
  @app.route('/questions')
  def retrieve_questions():
    try:
      selection=Question.query.order_by(Question.id).all()
      data = Category.query.order_by(Category.id).all()
      categories = [item.type for item in data]
      if len(selection) == 0:
        return jsonify({
          'questions': None,
          'total_questions': 0,
          'categories': categories,
          'current_category': None
        })
      else:
        current_questions = paginate_questions(request, selection)
        return jsonify({
          'questions': current_questions,
          'total_questions': len(selection),
          'categories': categories,
          'current_category': None
        })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
          abort(404)
      question.delete()
      return jsonify({
        'success': True
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods = ['POST'])
  def add_question():
    try:
      data = request.get_json()
      question = data['question']
      answer = data['answer']
      category = int(data['category']) + 1
      difficulty = data['difficulty']
      new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      new_question.insert()
      return jsonify({
        'success': True
        })
    except:
      abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods = ['POST'])
  def search_questions():
    try:
      data = request.get_json()
      search_term = data['searchTerm']
      selection = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
      if len(selection) == 0:
        abort(404)
      temp = []
      for item in selection:
        temp.append(item.format())
      return jsonify({
        'success': True,
        'questions': temp,
        'total_questions': len(selection),
        'current_category': None
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    #Have to add 1 to the category_id to offset frontend code index 0
    try:
      data = Question.query.filter(Question.category==category_id+1).all()
      if len(data) == 0:
        abort(404)
      temp = []
      for item in data:
        temp.append(item.format())
      return jsonify({
        'success': True,
        'questions': temp,
        'total_questions': len(temp),
        'current_category': category_id
      })
    except:
      abort(404)
    
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
  @app.route('/quizzes', methods = ['POST'])
  def play_quiz():
    try:
      data = request.get_json()
      previous_questions = data['previous_questions']

      #Using category type as fromtend assigns id 0 to both ALL amd Science
      quiz_category = data['quiz_category']['type'] 

      if quiz_category=='click':
        selection = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        selection = Question.query.join(Category, Category.id==Question.category).filter(Category.type==quiz_category, Question.id.notin_(previous_questions)).all()
      
      if len(selection) == 0:
        return jsonify({
          'success': False,
          'question': None
        })

      resp_data = random.choice(selection).format()
      return jsonify({
        'success': True,
        'question': resp_data
      })
    except:
      abort(400)
    
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
        "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500

  return app

    