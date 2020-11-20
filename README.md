# Django_good_hands

Django web apllication (PL):
The aim of the project was to create a place where everyone will be able to give unnecessary things to trusted 
institutions.
Live version: https://powerful-river-82273.herokuapp.com

## Requirements

To install all nesccesery iteams use following command line in terminal
while your virtual enviroment for this project is active:
```python
$ pip install -r requirements.txt
```

## Configuration 
 
Project uses django-environ. For configuration purposes, remove the sample tip 
from the .env.sample file and complete the file with your data.
```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
SECRET_KEY=<your-secret-key>
DATABASE_URL=<your-database-url>
EMAIL_HOST_USER=<your@email.host>
EMAIL_HOST_PASSWORD=<your-email-hots-pasw>
```
The project uses the Postgresql database system.
