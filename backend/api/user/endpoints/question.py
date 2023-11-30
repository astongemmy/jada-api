from models import Question, Category, format_questions
from werkzeug.exceptions import NotFound
from flask import request, abort
from ..utils import UserResource
from api.user import router
from ..router_models import (
  question_model_delete,
  question_model_write,
  questions_model
)

QUESTIONS_PER_PAGE = 10

@router.route('/questions', '/questions/<int:question_id>')
class Questions(UserResource):
  @router.marshal_with(questions_model)
  def get(self):
    page = request.args.get('page', 1, type = int)

    try:
      questions = Question.query.order_by(Question.id).paginate(page, QUESTIONS_PER_PAGE)

      categories = Category.query.all()
      
      all_categories = {}
      if len(categories) > 0:
        for category in categories:
          all_categories[category.id] = category.type

      return {
        'questions': format_questions(questions.items),
        'total_questions': questions.total,
        'categories': all_categories,
        'success': True
      }
    except NotFound:
      print('Question resource not found in the database.')
      abort(404)
    except Exception as error:
      print(error)
      abort(422)

  @router.marshal_with(question_model_write)
  def post(self):
    body = request.get_json()
    
    difficulty = body.get('difficulty', None)
    question = body.get('question', None)
    category = body.get('category', None)
    answer = body.get('answer', None)
    
    try:
      if not question or not answer: abort(422)
      
      question = Question(
        difficulty = difficulty,
        question = question,
        category = category,
        answer = answer
      )
      
      question.insert()
      
      return {
        'message': 'Question created successfully.',
        'success': True,
        **body
      }
    except Exception as error:
      print(error)
      abort(422)
  
  @router.marshal_with(question_model_delete)
  def delete(self, question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      question.delete()
      
      return {
        'message': 'Question deleted successfully.',
        'deleted': question_id,
        'success': True,
      }
    except NotFound:
      print('Question not found in the database.')
      abort(404)
    except Exception as error:
      print(error)
      abort(422)

@router.route('/questions/search')
class Search(UserResource):
  @router.marshal_with(questions_model)
  def get(self):
    search = request.args.get('q', None, type = str)
    page = request.args.get('page', 1, type = int)

    try:
      questions = Question.query.order_by(Question.id).filter(
        Question.question.ilike("%{}%".format(search))
      ).paginate(page, QUESTIONS_PER_PAGE)

      questions.format_multiple()

      return {
        'message': 'Search results returned successfully.',
        'questions': format_questions(questions.items),
        'total_questions': questions.total,
        'success': True
      }
    except Exception as error:
      print(error)
      abort(422)