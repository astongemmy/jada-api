from models import Question, Category, format_questions
from ...utils.response import ApiResponse
from sqlalchemy.exc import DataError
from ..utils import UserResource
from flask import request, abort
from api.user import router
from ..schema import (
  question_model_delete,
  question_model_write,
  question_model_read,
  questions_model
)

QUESTIONS_PER_PAGE = 10

@router.route('/questions/<int:question_id>', strict_slashes=True)
class Questionsy(UserResource):
  @router.marshal_with(question_model_read)
  def get(self, question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    if question == None:
      return ApiResponse.not_found(message='Question not found')
    
    return ApiResponse.ok(
      message='Question returned successfully',
      data={
        'question': question.format()
      }
    )

  @router.marshal_with(question_model_delete)
  def delete(self, question_id = ''):
    question = Question.query.filter(Question.id == question_id).one_or_none()
      
    if question == None:
      return ApiResponse.not_found(message='Question not found')

    question.delete()
      
    return ApiResponse.ok(
      message='Question deleted successfully',
      data={
        'deleted': question_id
      }
    )


@router.route('/questions')
class Questions(UserResource):
  @router.marshal_with(questions_model)
  def get(self):
    page = request.args.get('page', 1, type = int)
    
    questions = Question.query.order_by(Question.id).paginate(page, QUESTIONS_PER_PAGE)
    
    categories = Category.query.all()
    
    all_categories = {}
    if len(categories) > 0:
      for category in categories:
        all_categories[category.id] = category.type

    return ApiResponse.ok(
      message='Questions returned successfully',
      data={
        'questions': format_questions(questions.items),
        'total_questions': questions.total,
        'categories': all_categories
      }
    )
  
  @router.marshal_with(question_model_write)
  def post(self):
    required_fields = ['question', 'answer', 'category', 'difficulty']
    difficulty = self.api.payload.get('difficulty', None)
    question = self.api.payload.get('question', None)
    category = self.api.payload.get('category', None)
    answer = self.api.payload.get('answer', None)

    try:
      if not question or not answer:
        return ApiResponse.unprocessable(
          message='Necessary fields missing in request payload',
          data={
            'required_fields': required_fields,
            'payload': self.api.payload
          }
        )
      
      question = Question(
        difficulty = difficulty,
        question = question,
        category = category,
        answer = answer
      )
      
      question.insert()
      
      return ApiResponse.created(
        message='Question created successfully',
        data=self.api.payload
      )
    except DataError:
      data = { 'payload': self.api.payload }
      question.rollback()
      abort(422, data)


@router.route('/questions/search')
class Search(UserResource):
  @router.marshal_with(questions_model)
  def get(self):
    search = request.args.get('q', None, type = str)
    page = request.args.get('page', 1, type = int)
    
    questions = Question.query.order_by(Question.id).filter(
      Question.question.ilike("%{}%".format(search))
    ).paginate(page, QUESTIONS_PER_PAGE)
    
    return ApiResponse.ok(
      message='Search results returned successfully',
      data={
        'questions': format_questions(questions.items),
        'total_questions': questions.total,
      }
    )