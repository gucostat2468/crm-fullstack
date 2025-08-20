from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='Pendente')
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))