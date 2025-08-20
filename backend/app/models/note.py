from app import db
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))