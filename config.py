#import os
class Config:
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    #POSTGRES_URL = 'db:5432'
    #POSTGRES_URL = '192.168.189.32:41613'
    POSTGRES_URL = 'localhost:5432'
    POSTGRES_USER = 'postgres'
    POSTGRES_PW = 'docker'
    POSTGRES_DB = 'task_db'
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    FLASK_APP="app.py"

#  sudo docker run --rm  --name flask-db -e POSTGRES_PASSWORD=docker -d -p 5432:5432 postgres:12-alpine
# sudo docker exec -it flask-db psql -U postgres -c "create database task_db"
