from datetime import datetime, timezone

from app import db

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    images = db.relationship('Image', backref= 'project', lazy=True)
    # tasks = db.relationship('Task', backref= 'project', lazy=True)
    