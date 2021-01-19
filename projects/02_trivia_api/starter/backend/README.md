# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET ‘/categories/<int:category_id>/questions’
POST ‘/questions’
POST ‘/questions/search’
POST ‘/quizzes’
DELETE ‘/questions/<int:question_id>


GET '/categories'
- Fetches a list of categories in which each value is the corresponding string of the category
- Request Arguments: None
- Returns: A json object with two key:value pairs -- success and categories.
- Key ‘success’: Boolean corresponds to a Boolean value.
- Key ‘categories’ corresponds to a list of string values representing the category names ["Science", "Art", “Geography", "History", "Entertainment", "Sports"]

GET '/questions'
- Fetches all questions paginated by 10 questions per page along with the total number of questions, and a list of all categories
- Request Arguments: None
- Returns: A json object with 4 key:value pairs
    Key ‘questions’ corresponds to a list of dictionaries, where each dictionary represents a question as {
        ‘id’: Integer,
        ‘question’: String,
        ‘Answer’: String,
        ‘category’: Integer,
        ‘difficulty’; Integer
        }
    Key ‘total_questions’ corresponds to total number of questions (Integer)
    Key ‘categories’ corresponds to a list of string values representing the category names ["Science", "Art", “Geography", "History", "Entertainment", "Sports"]
    Key ‘current_category” is set to None

DELETE ‘/questions/<int:question_id>
- Deletes the question with id = question_id
- Request Arguments: question_id
- Returns: A json object with 1 key: value pair
- Key ‘success’ corresponds to a Boolean value

POST ‘/questions’
- Inserts a new question into the database
- Request Arguments: A json object with 4 key:value pairs 
    {
    ‘question’: String,
    ‘Answer’: String,
    ‘category’: Integer,
    ‘difficulty’; Integer
    }
- Returns: A json object with 1 key:value pairs
    {
    ‘success’: Boolean,
    }

POST ‘/questions/search’
- Searches for a given search term as a case-insensitive substring within each question
- Request Arguments: A json object with 1 key:value pair
    {
    ‘searchTerm: String
    }
- Returns: A json object with 4 key:value pairs
    Key ‘success’: Boolean
    Key ‘questions’ corresponds to a list of dictionaries, where each dictionary represents a question that contains the search term as a substring 
        {
        ‘id’: Integer,
        ‘question’: String,
        ‘Answer’: String,
        ‘category’: Integer,
        ‘difficulty’; Integer
        }
    Key ‘total_questions’ corresponds to total number of questions (Integer)
    Key ‘current_category” is set to None

GET ‘/categories/<int:category_id>/questions’
- Returns a list of questions belonging to the specified category
- Request Arguments: category_id, which is generated by the frontend
- Returns: A json object with 4 key:value pairs
    {
    ‘success’: Boolean,
    ‘questions’ corresponds to a list of dictionaries, where each dictionary represents a question as {
        ‘id’: Integer,
        ‘question’: String,
        ‘Answer’: String,
        ‘category’: Integer,
        ‘difficulty’; Integer
        },
    ‘total_questions’: Integer,
    ‘current_category’: Integer
    }

POST ‘/quizzes’
- Fetches a random question for the specified category provided it is not one of the previous questions
- Request Arguments: A json object with 2 key:value pairs
    {
    ‘previous_questions’: a list of integers corresponding to ids of previous questions,
    ‘Quiz_category’: a dictionary with 2 key:value pairs
        {
        ‘type’: String representing the category string,
        ‘id’: Integer representing the category
        }
    }
    
- Returns: A json object with 2 key:value pairs
    {
    ‘success’: Boolean,
    ‘question’: None if success = False, otherwise a dictionary with 5 key:value pairs 
        {
        ‘id’: Integer,
        ‘question’: String,
        ‘Answer’: String,
        ‘category’: Integer,
        ‘difficulty’; Integer
        }
    }


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
