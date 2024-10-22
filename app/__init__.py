from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

from config import configurations_by_environment

app = Flask(__name__)
app.config.from_object(configurations_by_environment['dev'])

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    
    # Bind the Flask application context to Celery
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Create Celery instance
celery = make_celery(app)

from app.routes import *
from app.model.project_model import *
from app.model.image_model import *