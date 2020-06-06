# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Style Guide

The Trivia API backend is written with PEP 8 as the style guide. Googles yapf formatter was used to format the code. For consistency, feel free to format using it. It can be installed with `pip install yapf` or view the [GitHub repo](https://github.com/google/yapf)

## Getting Started

### Quick Start

To jump in right away, follow the sections below. For more detailed instructions, view the readme files for the frontend and backend here:
1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

#### Frontend

```bash
# Change directory to the frontend directory if not already
cd ./frontend
npm install
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view the Trivia app in the browser. **Note**, the frontend will not function correctly until the backend is started.

#### Backend

To set up the backend API server:
```bash
# From the project root directory, setup the database. Depending on your psql instance configuration, this may change. Also, check the trivia.psql file to make sure the correct username is being used.
dropdb trivia && createdb trivia
psql trivia < trivia.psql
# Change directory to the backend directory
cd ./backend
# Install requirements in a virtual environment
pip install -r requirements.txt
# Prepare the Flask app to run.  Use 'set' instead of 'export' on Windows
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
