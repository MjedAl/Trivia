# Endpoints:

## GET '/categories'
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: ID and name of each category
  Example:
    Called with:
      curl http://127.0.0.1:5000/categories -X GET
    Response:
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "success": true
    }
```

## GET '/questions?page=<page_number>'
```
- Fetches a dictionary of questions and returns 10 questions based on the page number, total_questions, and categories.
- Optional Arguments: Page number
- Returns:
  Example:
    Called with:
      curl http://127.0.0.1:5000/questions -X GET
    Response:
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
    ],
    "success": true,
    "total_questions": 19
    }
```

## DELETE '/questions/<int:question_id>'
```
- Deletes the question with the given ID from the database
- Required Arguments: int:question_id
- Returns: the id of the deleted question and status
  Example:
    Called with:
      curl http://127.0.0.1:5000/questions/121 -X DELETE
    Response:
      {
        "deleted": 121,
        "success": true
      }
```


## POST '/questions'
```
- Adds a question to the DB and return the id of the new created question
- Required Arguments: body with the question information {
    question,answer,difficulty,category   
}
- Returns: Body with status and question id
  Example:
    Called with:
      curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"test?", "answer":"yes","difficulty":1,"category":1}'
    Response:
      {
        "question_id": 122,
        "success": true
      }
```

## POST '/questions/search?page=<page_number>'
```
- Search for a term in the database for the related questions the search is case insensitive
  and searches for a partial match.
- Required Arguments: body with the search term {
    searchTerm
}
- Optional Arguments: page=the page number
- Returns: JSON
    Example:
      Called with:
        curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"taJ"}'
      response:
        {
          "questions": [
            {
              "answer": "Agra",
              "category": 3,
              "difficulty": 2,
              "id": 15,
              "question": "The Taj Mahal is located in which Indian city?"
            }
          ],
          "success": true,
          "total_questions": 1
        }
```

## GET '/categories/<category_id>/questions?page=<page_number>'
```
- Returns the questions in the specified category with the list of categories
- Required Arguments: category_id
- Optional Arguments: page_number
- Returns:
  Example:
    Called with:
      curl http://127.0.0.1:5000/categories/1/questions -X GET
    Response:
      {
        "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
        },
        "current_category": "1",
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
          },
          {
            "answer": "yes",
            "category": 1,
            "difficulty": 1,
            "id": 122,
            "question": null
          }
        ],
        "success": true,
        "total_questions": 4
      }
```

## POST '/quizzes'
```
- Returns the a non reparative question based on the previous questions and the category if given
- Required Arguments: None
- Optional Arguments: in the body: {quiz_category, previous_questions}
- Returns:
  Example:
    Called with:
      curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"sports", "id":"6"}, "previous_questions":[10]}'
    Response:
      {
        "Success": true,
        "question": {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        }
      }
```
