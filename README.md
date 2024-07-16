# Guest Book

## Installation 
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

# APIs

Get List of Entry: 
```
curl -X GET http://127.0.0.1:8000/api/entries/
```
Get User's Data: 
```
curl -X GET http://127.0.0.1:8000/api/users/
```
Create Entry: 
```
curl -X POST -d '{ "user": { "name": "New User" }, "subject": "New Entry", "message": "This is a new entry." }' http://127.0.0.1:8000/api/create_entry/ -H "Content-Type: application/json"

```


