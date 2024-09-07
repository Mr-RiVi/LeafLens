from datetime import datetime, timezone

from app import db

class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False) # db.ForeignKey('project.project_id') class name in lowercase and its id