from datetime import datetime, timezone
from app import db

class AnalysisResult(db.Model):
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    result_data = db.Column(db.JSON, nullable=False)
    analysis_timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
