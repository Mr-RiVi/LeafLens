from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import configurations_by_environment

app = Flask(__name__)
app.config.from_object(configurations_by_environment['dev'])

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.routes import *
from app.model.project_model import *
from app.model.image_model import *