from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Enum
from datetime import datetime, timezone

from config import db


class Problem(db.Model, SerializerMixin):
    __tablename__ = 'problems'

    serialize_rules = ('-user.problems', '-attempts.problem')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(
        Enum('Easy', 'Medium', 'Hard', name='difficulty_enum'),
        nullable=False
    )
    problem_type = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='problems')
    attempts = db.relationship('Attempt', back_populates='problem', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Problem {self.name} [{self.difficulty}]>'
