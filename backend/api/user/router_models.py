from flask_restx import fields
from .main import router

request_model = router.model('Request', {
  'message': fields.String(
    default='Your request was not successful.',
    description='Response message.'
  ),
  'success': fields.Boolean(
    description='Request completion status.',
    default=False
  )
})

category_model = router.model('Category', {
  'id': fields.Integer(description='Unique category identifier.'),
  'type': fields.String(description='Category text.')
})

categories_model = router.inherit('Category', request_model, {
  'categories': fields.Raw(
    description='Object of all question categories.',
    default={}
  )
})

question_model_base = router.model('Question', {
  'difficulty': fields.Integer(description="Question's difficulty level."),
  'category': fields.Integer(description="Category.s unique identifier."),
  'question': fields.String(description='Question to be answered.'),
  'answer': fields.String(description="Question's answer.")
})

question_model_write = router.inherit('Question', request_model, question_model_base)

question_model_delete = router.inherit('Question', request_model, {
  'deleted': fields.Integer(description="Deleted question's unique identifier.")
})

question_model_read = router.inherit('Question', question_model_base, {
  'id': fields.Integer(description='Unique question identifier.')
})

category_questions_model = router.inherit('Category', request_model, {
  'questions': fields.List(fields.Nested(question_model_read)),
  'total_questions': fields.Integer(
    description='Total number of questions retrieved.',
    default=0
  ),
  'current_category': fields.String(
    description="Current questions' category.",
    default=None
  )
})

questions_model = router.inherit('Questions', request_model, {
  'questions': fields.List(fields.Nested(question_model_read)),
  'total_questions': fields.Integer(
    description='Total number of questions retrieved.',
    default=0
  ),
  'current_category': fields.String(
    description="Current questions' category.",
    default=None
  ),
  'categories': fields.Raw(
    description='Object of all question categories.',
    default={}
  )
})

quiz_questions_model = router.inherit('QuizQuestion', request_model, {
  'question': fields.Raw(
    description='Object of retrieved question to play quiz.',
    default={}
  )
})