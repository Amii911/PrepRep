# PrepRep

A full-stack web application for tracking LeetCode problem progress. Built with a React frontend and a Flask/SQLite backend.

## Tech Stack

- **Frontend:** React, React Router
- **Backend:** Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate
- **Database:** SQLite

## Project Structure

```
.
├── client/          # React frontend
│   ├── public/
│   └── src/
└── server/          # Flask backend
    ├── app.py       # Routes and entry point
    ├── config.py    # App configuration
    ├── models.py    # Database models
    └── seed.py      # Database seed data
```

## Setup

### Backend

Install dependencies and activate the virtual environment:

```bash
pipenv install
pipenv shell
```

Initialize the database:

```bash
cd server
flask db init
flask db upgrade head
```

Optionally seed the database:

```bash
python seed.py
```

Run the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5555`.

### Frontend

Install dependencies:

```bash
npm install --prefix client
```

Run the React app:

```bash
npm start --prefix client
```

The app will be available at `http://localhost:3000`.
