from flask import Flask
app = Flask(__name__)

import os
import studentapp.config as config
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['TEMPLATES_AUTO_RELOAD'] = True


from studentapp.models import db
db.app = app
db.init_app(app)

import studentapp.controllers
