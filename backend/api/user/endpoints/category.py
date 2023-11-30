from ..router_models import categories_model, category_questions_model
from models import Category, Question, format_questions
from werkzeug.exceptions import NotFound
from ..utils import UserResource
from api.user import router
from flask import abort

@router.route('/categories', '/categories/<int:category_id>/questions')
class Categories(UserResource):
  @router.marshal_with(categories_model)
  def get(self):
    try:
      categories = Category.query.all()
      
      all_categories = {}
      
      for category in categories:
        all_categories[category.id] = category.type
        
      return {
        'message': 'Categories returned successfully.',
        'categories': all_categories,
        'success': True,
      }
    except NotFound:
      print('Category resource not found in the database.')
      abort(404)
    except Exception as error:
      print(error)
      abort(422)

  @router.marshal_with(category_questions_model)
  def post(self, category_id = ''):
    try:
      questions = Question.query.filter(Question.category == category_id).all()
      
      return {
        'message': 'Category questions returned successfully.',
        'questions': format_questions(questions),
        'total_questions': len(questions),
        'current_category': None,
        'success': True
      }
    except Exception as error:
      print(error)
      abort(422)