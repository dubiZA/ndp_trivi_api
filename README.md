# Full Stack Trivia - Final API Project

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

To jump in right away, follow the sections below. For more detailed instructions, view the readme files for the frontend and backend here:
+ [`./frontend/`](./frontend/README.md)
+ [`./backend/`](./backend/README.md)

The `./backend` documentation covers how to run the test suite.

### Frontend

```bash
# Change directory to the frontend directory if not already
cd ./frontend
npm install
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view the Trivia app in the browser. **Note**, the frontend will not function correctly until the backend is started.

### Backend

To set up the backend server:
```bash
# From the project root directory, setup the database.
# Depending on your psql instance configuration, this may change.
# Also, check the trivia.psql file to make sure the correct username is being used.
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

# API Reference

The Trivia application is powered by a Python Flask RESTful API on the backend. This API follows RESTful principles, using standard HTTP verbs (GET, POST, DELETE, etc) and returning response as JSON.

## Getting Started

The base URL for the API backend is http://localhost:5000/api/v1/

There is no authentication required for this API or any of it's endpoints at this time

## Errors

Clients should expect to recieve one of several types of HTTP error response codes if something goes wrong or a request is not correctly submitted. Error response messages are returned as JSON. Response codes include:

+ `400` Bad Request
+ `404` Not Found
+ `405` Method Not Allowed
+ `422` Unprocessable

The JSON error response will have the following structure:

```javascript
{
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
}
```

## Endpoint Reference

What follows is the API endpoint reference. The URL pattern would be \[base_url\]/endpoint, for example:
<http://localhost:5000/api/v1/questions>

### GET /api/v1/categories

Handles requests for categories. When a request is submitted to this endpoint, all categories in the database will be sent to the user in a JSON response.

The JSON response is an object with keys and values:
+ success: True (bool)
+ categories: (JSON object)
    + category_id: category_name (string)

```javascript
{
    'success': True,
    'categories': {
        '1': 'Science',
        '2': 'History',
        '3': 'etc'
    }
}
```

