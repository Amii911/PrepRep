#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api
from models.user import User


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


class Users(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all()]
        return make_response(users, 200)

    def post(self):
        data = request.get_json()
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=data['password_hash'],
            )
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 422)


class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({'error': 'User not found'}, 404)
        return make_response(user.to_dict(), 200)

    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({'error': 'User not found'}, 404)
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return make_response(user.to_dict(), 200)
        except Exception as e:
            return make_response({'error': str(e)}, 422)

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({'error': 'User not found'}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

