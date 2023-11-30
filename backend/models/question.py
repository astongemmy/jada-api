from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Question model
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    category = Column(String)
    question = Column(String)
    answer = Column(String)

    def __init__(self, question, answer, category, difficulty):
        self.difficulty = difficulty
        self.question = question
        self.category = category
        self.answer = answer

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'difficulty': self.difficulty,
            'question': self.question,
            'category': self.category,
            'answer': self.answer,
            'id': self.id,
        }
    

def format_questions(questions):
    return [question.format() for question in questions]