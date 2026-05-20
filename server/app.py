
from flask import request, make_response, session
from flask_restful import Resource
from config import app, db, api
from models.user import User
from models.problem import Problem
from models.attempt import Attempt

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
                password_hash=data['password'],
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


class Problems(Resource):
    def get(self):
        problems = [p.to_dict() for p in Problem.query.all()]
        return make_response(problems, 200)

    def post(self):
        data = request.get_json()
        try:
            problem = Problem(
                name=data['name'],
                difficulty=data['difficulty'],
                problem_type=data['problem_type'],
                url=data.get('url'),
                notes=data.get('notes'),
                user_id=data['user_id'],
            )
            db.session.add(problem)
            db.session.commit()
            return make_response(problem.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 422)


class ProblemById(Resource):
    def get(self, id):
        problem = Problem.query.get(id)
        if not problem:
            return make_response({'error': 'Problem not found'}, 404)
        return make_response(problem.to_dict(), 200)

    def patch(self, id):
        problem = Problem.query.get(id)
        if not problem:
            return make_response({'error': 'Problem not found'}, 404)
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(problem, key, value)
            db.session.commit()
            return make_response(problem.to_dict(), 200)
        except Exception as e:
            return make_response({'error': str(e)}, 422)

    def delete(self, id):
        problem = Problem.query.get(id)
        if not problem:
            return make_response({'error': 'Problem not found'}, 404)
        db.session.delete(problem)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(Problems, '/problems')
api.add_resource(ProblemById, '/problems/<int:id>')


class Attempts(Resource):
    def get(self):
        attempts = [a.to_dict() for a in Attempt.query.all()]
        return make_response(attempts, 200)

    def post(self):
        data = request.get_json()
        try:
            attempt = Attempt(
                status=data['status'],
                time_taken=data.get('time_taken'),
                solution_notes=data.get('solution_notes'),
                language=data.get('language'),
                problem_id=data['problem_id'],
            )
            db.session.add(attempt)
            db.session.commit()
            return make_response(attempt.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 422)


class AttemptById(Resource):
    def get(self, id):
        attempt = Attempt.query.get(id)
        if not attempt:
            return make_response({'error': 'Attempt not found'}, 404)
        return make_response(attempt.to_dict(), 200)

    def patch(self, id):
        attempt = Attempt.query.get(id)
        if not attempt:
            return make_response({'error': 'Attempt not found'}, 404)
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(attempt, key, value)
            db.session.commit()
            return make_response(attempt.to_dict(), 200)
        except Exception as e:
            return make_response({'error': str(e)}, 422)

    def delete(self, id):
        attempt = Attempt.query.get(id)
        if not attempt:
            return make_response({'error': 'Attempt not found'}, 404)
        db.session.delete(attempt)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(Attempts, '/attempts')
api.add_resource(AttemptById, '/attempts/<int:id>')


class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=data['password'],
            )
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return make_response(user.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 422)


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return make_response(user.to_dict(), 200)
        return make_response({'error': 'Invalid username or password'}, 401)


class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return make_response({}, 204)


class Me(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Not logged in'}, 401)
        user = User.query.get(user_id)
        if not user:
            return make_response({'error': 'User not found'}, 401)
        return make_response(user.to_dict(), 200)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Me, '/me')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

