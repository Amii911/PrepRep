from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

from config import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-_password_hash', '-problems.user', '-attempts.problem.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column('password_hash', db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        password = kwargs.pop('password_hash', None)
        super().__init__(**kwargs)
        if password:
            self.password_hash = password

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self._password_hash, password)

    problems = db.relationship('Problem', back_populates='user', cascade='all, delete-orphan')
    attempts = association_proxy('problems', 'attempts')

    def __repr__(self):
        return f'<User {self.username}>'
