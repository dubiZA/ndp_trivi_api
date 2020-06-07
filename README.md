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

Sample request: `curl http://localhost:5000/api/v1/categories`

The JSON response is an object with keys and values:
+ success: True (boolean)
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


### GET /api/v1/questions

Handles requests for questions. When a request is submitted to this endpoint, all questions in the database will be sent to the user in a JSON response with additional data that may be useful to the requesting client. This endpoint returns a paginated response with a hardcoded page size of 10 items per page.

Sample request: `curl http://localhost:5000/api/v1/questions`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ questions: (array of JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ categories: (JSON object)
    + category_id: category_name (string)
+ current_category: None
+ total_questions: (int)
+ current_page: (int)

```javascript
{
    'success': True,
    'questions': [
        {
            'id': 1,
            'questions': 'Foo',
            'answer': 'Bar',
            'category' 'Baz',
            'Difficulty': 1
        },
        {
            'id': 2,
            'questions': 'Baz',
            'answer': 'Bar',
            'category' 'Foo',
            'Difficulty': 4
        }
    ],
    'categories': {
        '1': 'Science',
        '2': 'History',
        '3': 'etc'
    },
    'current_category': None,
    'total_questions': 2,
    'current_page': 1
}
```

### DELETE /api/v1/questions/[question_id]

Handles delete requests for a specific question in the questions collection. When a request is submitted to this endpoint, the question is looked up in the database and deleted from. A JSON response is sent to the user to confirm the delete action with additional data that may be useful to the requesting client, like all the questions remaining in the database, count of all questions remaining and the current page number. This endpoint takes an integer as the final part of the URL.

Sample request: `curl -X DELETE http://localhost:5000/api/v1/questions/1`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ deleted: (int)
+ questions: (array of JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ total_questions: (int)
+ current_page: (int)

```javascript
{
    'success': True,
    'deleted': 1
    'questions': [
        {
            'id': 2,
            'questions': 'Baz',
            'answer': 'Bar',
            'category' 'Foo',
            'Difficulty': 1
        }
    ],
    'total_questions': 1,
    'current_page': 1
}
```
If the question cannot be deleted an error is returned. If they question does not exist in the database a 404 is returned.

### POST /api/v1/questions

Handles POST requests for either:
+ Creating a new question in the database
+ Searching for an existing question by question text with partial matches supported

#### Creating a new question

When a search term is not found in the POST request, the endpoint will take a POST request for a new question. The payload should have the following keys and value data types:
+ question: (string)
+ answer: (string)
+ category: (int)
+ difficulty: (int)

Sample request: `curl -X POST -H 'Content-Type: application/json' -d '{"question": "Foo", "answer": "Bar", "category": "1", "difficulty": "2"}' http://localhost:5000/api/v1/questions/`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ questions: (array of JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ total_questions: (int)
+ current_page: (int)

```javascript
{
    'success': True,
    'questions': [
        {
            'id': 2,
            'questions': 'Baz',
            'answer': 'Bar',
            'category' 'Foo',
            'Difficulty': 1
        },
        {
            'id': 3,
            'questions': 'Foo',
            'answer': 'Bar',
            'category' 'Baz',
            'Difficulty': 2
        }
    ],
    'total_questions': 2,
    'current_page': 1
}
```
If the question cannot be added an error is returned.

#### Searching for a question

When a search term is found in the POST request, the endpoint will request any questions matching the submitted string from the database. The search term is not case sensitive. The payload should have the following key and value data type:
+ searchTerm: (string)

Sample request: `curl -X POST -H 'Content-Type: application/json' -d '{"searchTerm": "foo"}' http://localhost:5000/api/v1/questions/`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ questions: (array of JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ total_questions: (int)
+ current_page: (int)

```javascript
{
    'success': True,
    'questions': [
        {
            'id': 3,
            'questions': 'Foo',
            'answer': 'Bar',
            'category' 'Baz',
            'Difficulty': 2
        }
    ],
    'total_questions': 2,
    'current_page': 1
}
```
If the search term cannot be found an error is returned.

### GET /api/v1/categories/[category_id]/questions

Handles GET requests for a specific category and all related questions in the collection. When a request is submitted to this endpoint, the category is looked up in the database and only questions with a matching category ID are returned. A JSON response is sent to the user with the questions for the specified category as well as a count of all questions remaining and the current page number.

Sample request: `curl http://localhost:5000/api/v1/categories/3/questions`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ questions: (array of JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ categories: (JSON object)
    + category_id: category_name (string)
+ current_category: (string)
+ total_questions: (int)
+ current_page: (int)

```javascript
{
    'success': True,
    'questions': [
        {
            'id': 1,
            'questions': 'Foo',
            'answer': 'Bar',
            'category' 'Baz',
            'Difficulty': 1
        },
        {
            'id': 2,
            'questions': 'Baz',
            'answer': 'Bar',
            'category' 'Baz',
            'Difficulty': 4
        }
    ],
    'categories': {
        '1': 'Science',
        '2': 'History',
        '3': 'Baz'
    },
    'current_category': 'Baz',
    'total_questions': 2,
    'current_page': 1
}
```
If the category or questions cannot be found in the database a 404 is returned.

### POST /api/v1/quizzes

Handles GET requests for the quiz game. When a request is submitted to this endpoint, the category is looked up in the database and only questions with a matching category are returned. A JSON response is sent to the user with a randomly chosen question for the specified category as well as a count of all questions remaining in the question set. The endpoint also take a list of previously asked questions and excludes them from the question pool with each subsequent request to the endpoint.

Sample request: `curl -X POST -H 'Content-Type: application/json' -d '{"quiz_category": "Foo", "previous_questions": "[]"}' http://localhost:5000/api/v1/quizzes/`

The JSON response is an object with the keys and value data types:
+ success: (boolean)
+ question: (JSON objects)
    + id: (int)
    + question: (string)
    + answer: (string)
    + category: (string)
    + difficulty: (int)
+ remaining_questions: (int)

```javascript
{
    'success': True,
    'question': {
        'id': 1,
        'questions': 'Foo',
        'answer': 'Bar',
        'category' 'Baz',
        'Difficulty': 1
    },
    'remaining_questions': 2
}
```
If there are no question for the selected category, a 404 is returned.