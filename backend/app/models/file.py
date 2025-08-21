from app import db
import datetime

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    size = db.Column(db.String(20))
    path = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))