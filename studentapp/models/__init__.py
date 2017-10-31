from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from studentapp.models.userlogin import UserLogin
from studentapp.models.buttonclicks import ButtonClicks