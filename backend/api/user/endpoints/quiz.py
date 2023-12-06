from ..schema import quiz_questions_model
from ...utils.response import ApiResponse
from sqlalchemy import and_, func
from ..utils import UserResource
from api.user import router
from models import Question
from flask import request

@router.route('/quizzes')
class Quizzes(UserResource):
  @router.marshal_with(quiz_questions_model)
  def post(self):
    body = request.get_json()
    
    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', None)
    
    question = Question.query.filter(
      and_(
        Question.category == quiz_category['id'] if quiz_category['id'] else Question.category > 0,
        Question.id.notin_(previous_questions)
      )
    ).order_by(func.random()).first()

    return ApiResponse.ok(
      message='Quiz question returned successfully.',
      data={
        'question': question.format() if question else {},
      }
    )