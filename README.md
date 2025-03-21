# JADA Server

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

###  Base URL
```
http://localhost:5000
```
Or any other URL explicitly set by choice.

####  Note: All successful requests return a JSON object containing a `success` field of `true` and `message` field reflecting the operation performed, alongside other key/value pairs for an endpoint.
##### Example
```json
{
  "success": true,
  "message": "Successful operation message.",
  "other_keys": "...other related field values"
}
```

### Endpoints

#### Get All Question Categories

`GET '/categories'`

- Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category type.
- Request Body: None
- Request Arguments: None
- Path Variables: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs shown below.

```json
{
  "success": true,
  "message": "Categories returned successfully.",
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### Get All Questions

`GET '/questions'`

- Description: Fetches a list of 10 questions per request, in a dictionary format containing keys and corresponding values. Also, this endpoint returns a dictionary of all question categories same as `/categories` endpoint, a total of all questions, as well as the current category.
- Request Body: None
- Request Arguments: Optional: `page` Type: Integer. Indicates what range of questions should be returned.
- Path Variables: None
- Returns: An object of key/value pairs, including a list of questions, number of total questions, current category and categories dictionary etc.

```json
{
  "success": true,
  "message": "Questions returned successfully.",
  "total_questions": 19,
  "current_category": "Art",
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ]
}
```

#### Delete a Question

`DELETE '/questions/:id'`

- Description: Deletes a question record from the database by referencing its id.
- Request Body: None
- Request Arguments: None
- Path Variables: Required `id` Type: Integer. Specifies which question exactly should be deleted.
- Returns: An object indicating a successful operation with the question id that was deleted.

```json
{
  "success": true,
  "message": "Question deleted successfully.",
  "deleted": 1
}
```

#### Get Category Questions

`GET '/categories/:id/questions'`

- Description: Fetches a list of category questions specified by id.
- Request Body: None
- Request Arguments: None
- Path Variables: Required `id` Type: Integer. Indicates which category questions should be retrieved.
- Returns: An object with category questions, total questions for specified category and current category.

```json
{
  "success": true,
  "message": "Category questions returned successfully.",
  "current_category": "Science",
  "total_questions": 3,
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ]
}
```

#### Create New Question

`POST '/questions'`

- Description: This endpoint creates a new question record in the database.
- Request Body: Required JSON object of question payload with keys/value pairs as below.
```json
{
  "question": "What is the heaviest organ in the human body?",
  "answer": "The Liver",
  "difficulty": "4",
  "category": "1"
}
```
- Request Arguments: None
- Path Variables: None
- Returns: An object of created question with success status of true and corresponding success message.

```json
{
  "success": true,
  "message": "Question created successfully.",
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }
}
```

#### Search questions

`POST '/questions/search'`

- Description: Returns a list of questions matching a case insensitive search term provided in the request body.
- Request Body: Required: JSON object of question search term.
```json
{
  "searchTerm": "organ"
}
```
- Request Arguments: None
- Path Variables: None
- Returns: An object containing total number of matching questions, current category, and a list of matching questions with respect to provided search term.

```json
{
  "success": true,
  "message": "Search questions returned successfully.",
  "total_questions": 1,
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ]
}
```

####  Play Quiz

`POST '/quizzes'`

- Description: This endpoint fetches a question to play the actual quiz. It takes category object and previous questions list parameters and then returns a random question within the specified category. If category and previous questions parameters are provided, returned question must be a question belonging to that category but not having an id found in previous questions list.
- Request Body: Required: JSON object of quiz question payload.
```json
{
  "quiz_category": {
    "id": 1,
    "type": "Science"
  },
  "previous_questions": ["20", "21"]
}
```
- Request Arguments: None
- Path Variables: None
- Returns: An object of randomly selected category question, if `quiz_category` field was provided or question of any category, if no `quiz_category` was provided.

```json
{
  "success": true,
  "message": "Quiz question returned successfully.",
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }
}
```

### Error Responses

Trivia API returns the following error responses with appropriate status codes as illustrated below.

####  400 Bad Request Error
- Description: This error is returned when there is a wrongly formatted request sent to the server.
- Returns: JSON object of the form.
```json
{
  "status": false,
  "error": "400",
  "message": "bad request"
}
```

####  404 Resource Not Found Error
- Description: This error is returned when a resource requested does not exist.
- Returns: JSON object of the form.
```json
{
  "status": false,
  "error": "404",
  "message": "resource not found"
}
```

####  405 Method Not Allowed Error
- Description: This error is returned when a resource is requested using a wrong http method.
- Returns: JSON object of the form.
```json
{
  "status": false,
  "error": "405",
  "message": "method not allowed"
}
```

####  422 Unprocessable Entity Error
- Description: This error is returned when a request can not be processed by the server due to maybe data error etc.
- Returns: JSON object of the form.
```json
{
  "status": false,
  "error": "422",
  "message": "unprocessable"
}
```

####  500 Server Error
- Description: This error is returned when the server is not able to process a request for some reasons.
- Returns: JSON object of the form.
```json
{
  "status": false,
  "error": "500",
  "message": "server error"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
