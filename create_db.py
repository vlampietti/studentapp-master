import os
from config import basedir
from studentapp import app
from studentapp.models import *
import pandas as pd


if __name__ == '__main__':
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
	db.create_all()
