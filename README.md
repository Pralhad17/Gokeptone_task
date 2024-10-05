install virtual enviornment
install requirements.txt file

 # Django 
makemigrations
migrate
runserver

Admin : username - admin
        Password - 123              

 # admin can view all tasks while regular users can only see their tasks
 # all users can perform CRUD Operations.

 Testing Using Postman Tool
 
Register 
Endpoint: Post http://127.0.0.1:8000/api/register/

Login 
Endpoint: Post http://127.0.0.1:8000/api/login/

Read
Endpoint: GET http://127.0.0.1:8000/api/tasks/


Create a Task
Endpoint: Post http://127.0.0.1:8000/api/tasks/

Update a Task
Endpoint: PUT http://127.0.0.1:8000/api/tasks/{task_id}/

Delete a Task
Endpoint: DELETE http://127.0.0.1:8000/api/tasks/{task_id}/

Additional Testing with Filters and Searches

Filtering by Status
Endpoint: GET http://127.0.0.1:8000/api/tasks/?status=Todo
Filtering by Priority
Endpoint: GET http://127.0.0.1:8000/api/tasks/?priority=High
Filtering by Due Date
Endpoint: GET http://127.0.0.1:8000/api/tasks/?due_date=2024-10-15
Searching Tasks
Endpoint: GET http://127.0.0.1:8000/api/tasks/?search=Task

Pagination Testing 👍

http://127.0.0.1:8000/api/tasks/?page=2


