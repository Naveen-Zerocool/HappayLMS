**Happay LMS APIs**

1. Available APIs:
   1. Add an author, category or a book
   2. List all authors, categories and books
   3. Get details of individual author, category or book
   4. Get most sold book by author or category
   5. Search books by author, category or author name and book name. All these searches works togeather as well
2. All book store related APIs are authenticated (Token Authentication)
3. Added register and login APIs
4. Handled general exception via a middleware
5. Added admin module with search and filter for book store models
6. Used sqlite as db

**Prerequisites**
1. Python 3.7.9

**Running on local machine**
1. sudo pip install virtualenv
2. virtualenv -p python3 happy-lms-venv
3. source happy-lms-venv/bin/activate
4. git clone <repo_link>
5. pip install -r requirements.txt
6. python3 manage.py migrate
7. python3 manage.py createsuperuser
8. python3 manage.py runserver

**Admin Site:** http://127.0.0.1:8000/admin/

**API Documentation:** [link_to_file](https://docs.google.com/spreadsheets/d/1uPbK5iZ8_DkrSXxe4YYgawlPwM2DVXpUQG1RZ2PBpp8/edit?usp=sharing)

**Postman collection:** Postman collection and environment JSON files are in the repo. Kindly import environment and API collection to try out the APIs. Have used random generators where ever possible, so API collection should be easy to try. 

On postman collection have added a test case for checking if the response code is 200 for all the requests, so we can use runner to execute all APIs available at once.

API Collection: [Happay LMS API Environment.postman_environment.json](Happay LMS API Environment.postman_environment.json)

Postman Environment: [Happay LMS APIs.postman_collection.json](Happay LMS APIs.postman_collection.json)

**Swagger API Doc:** http://127.0.0.1:8000/docs/

Swagger Document is not accurate and neat, due to time constrains have not proceeded with it.
