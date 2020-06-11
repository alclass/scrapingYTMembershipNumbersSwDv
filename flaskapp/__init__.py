'''
https://blog.miguelgrinberg.com/category/Flask
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    Chapter 1: Hello, World!
    Chapter 2: Templates
    Chapter 3: Web Forms
    Chapter 4: Database (this article)
    Chapter 5: User Logins
    Chapter 6: Profile Page and Avatars
    Chapter 7: Error Handling
    Chapter 8: Followers
    Chapter 9: Pagination
    Chapter 10: Email Support
    Chapter 11: Facelift
    Chapter 12: Dates and Times
    Chapter 13: I18n and L10n
    Chapter 14: Ajax
    Chapter 15: A Better Application Structure
    Chapter 16: Full-Text Search
    Chapter 17: Deployment on Linux
    Chapter 18: Deployment on Heroku
    Chapter 19: Deployment on Docker Containers
    Chapter 20: Some JavaScript Magic
    Chapter 21: User Notifications
    Chapter 22: Background Jobs
    Chapter 23: Application Programming Interfaces (APIs)
'''
from flask import Flask
from config import FlaskConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(FlaskConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flaskapp import routes, models


