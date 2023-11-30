from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Category model
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'type': self.type,
            'id': self.id,
        }

def format_categories(categories):
    return [category.format() for category in categories]