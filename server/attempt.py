from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Enum
from datetime import datetime

from config import db


class Attempt(db.Model, SerializerMixin):
    __tablename__ = 'attempts'

    serialize_rules = ('-problem.attempts',)

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        Enum('Solved', 'Attempted', 'Unsolved', name='status_enum'),
        nullable=False
    )
    date = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)
    solution_notes = db.Column(db.Text)
    language = db.Column(db.String)

    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)

    problem = db.relationship('Problem', back_populates='attempts')

    def __repr__(self):
        return f'<Attempt {self.status} on Problem {self.problem_id}>'
