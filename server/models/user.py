from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime, timezone

from config import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-problems.user', '-attempts.problem.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    problems = db.relationship('Problem', back_populates='user', cascade='all, delete-orphan')
    attempts = association_proxy('problems', 'attempts')

    def __repr__(self):
        return f'<User {self.username}>'
