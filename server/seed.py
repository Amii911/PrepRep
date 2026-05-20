#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from config import app, db
from models.user import User
from models.problem import Problem
from models.attempt import Attempt

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        Attempt.query.delete()
        Problem.query.delete()
        User.query.delete()

        difficulties = ['Easy', 'Medium', 'Hard']
        problem_types = ['Array', 'String', 'Tree', 'Graph', 'Dynamic Programming', 'Hash Table']
        statuses = ['Solved', 'Attempted', 'Unsolved']
        languages = ['Python', 'JavaScript', 'Java', 'C++']

        users = []
        for _ in range(3):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password_hash='password123',
            )
            db.session.add(user)
            users.append(user)

        db.session.commit()

        problems = []
        for user in users:
            for _ in range(4):
                problem = Problem(
                    name=fake.sentence(nb_words=4).rstrip('.'),
                    difficulty=rc(difficulties),
                    problem_type=rc(problem_types),
                    url=fake.url(),
                    notes=fake.text(max_nb_chars=100),
                    user_id=user.id,
                )
                db.session.add(problem)
                problems.append(problem)

        db.session.commit()

        for problem in problems:
            for _ in range(randint(1, 3)):
                attempt = Attempt(
                    status=rc(statuses),
                    time_taken=randint(5, 120),
                    solution_notes=fake.text(max_nb_chars=150),
                    language=rc(languages),
                    problem_id=problem.id,
                )
                db.session.add(attempt)

        db.session.commit()
        print("Done seeding!")
