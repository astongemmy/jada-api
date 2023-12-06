from flask_restx import fields
from .main import router

category_model = router.model('Category', {
  'id': fields.Integer(description='Unique category identifier.'),
  'type': fields.String(description='Category text.')
})

question_model = router.model('Question', {
  'difficulty': fields.Integer(description="Question's difficulty level."),
  'category': fields.Integer(description="Category.s unique identifier."),
  'question': fields.String(description='Question to be answered.'),
  'id': fields.Integer(description='Unique question identifier.'),
  'answer': fields.String(description="Question's answer.")
})

response_model = router.model('Response', {
  'message': fields.String(
    default='Your request was not successful.',
    description='Response message.'
  ),
  'success': fields.Boolean(
    description='Request completion status.',
    default=False
  ),
  'data': fields.Raw(
    description='Response data envelope.',
    default={}
  )
})


categories_data_model = router.inherit('CategoryResponseData', category_model, {
  'questions': fields.List(fields.Nested(question_model)),
  'total_questions': fields.Integer(
    description='Total number of questions retrieved.',
    default=0
  ),
  'categories': fields.Raw(
    description='Object of all question categories.',
    default={}
  ),
  'current_category': fields.String(
    description="Current questions' category.",
    default=None
  ),
})

question_data_model = router.inherit('QuestionResponseData', question_model, {
  'deleted': fields.Integer(description="Deleted question's unique identifier."),
  'required_fields': fields.List(
    description='Shows a list of required fields in request payload.',
    cls_or_instance=fields.String
  ),
  'payload': fields.Raw(
    description='A copy of request payload.',
    default={}
  )
})

quiz_data_model = router.inherit('QuizResponseData', question_model, {
  'question': fields.Raw(
    description='Object of retrieved question to play quiz.',
    default={}
  )
})


category_questions_model = router.inherit('CategoryQuestions', response_model, {
  'data': fields.Nested(question_data_model)
})

question_model_delete = router.inherit('DeleteQuestion', response_model, {
  'data': fields.Nested(question_data_model)
})

question_model_write = router.inherit('CreateQuestion', response_model, {
  'data': fields.Nested(question_data_model)
})

quiz_questions_model = router.inherit('QuizQuestion', response_model, {
  'data': fields.Nested(quiz_data_model)
})

question_model_read = router.inherit('GetQuestion', response_model, {
  'data': fields.Nested(question_data_model)
})

categories_model = router.inherit('Categories', response_model, {
  'data': fields.Nested(categories_data_model)
})

questions_model = router.inherit('GetQuestions', response_model, {
  'data': fields.Nested(question_data_model)
})