from ..schema import categories_model, category_questions_model
from models import Category, Question, format_questions
from ...utils.response import ApiResponse
from ..utils import UserResource
from api.user import router

@router.route('/categories')
class Categories(UserResource):
  @router.marshal_with(categories_model)
  def get(self):
    categories = Category.query.all()
    
    all_categories = {}
    
    for category in categories:
      all_categories[category.id] = category.type
      
    return ApiResponse.ok(
      message='Categories returned successfully.',
      data={
        'categories': all_categories
      }
    )


@router.route('/categories/<int:category_id>/questions')
class CategoryQuesitons(UserResource):
  @router.marshal_with(category_questions_model)
  def get(self, category_id = ''):
    questions = Question.query.filter(Question.category == category_id).all()
    
    return ApiResponse.ok(
      message='Category questions returned successfully.',
      data={
        'questions': format_questions(questions),
        'total_questions': len(questions)
      }
    )