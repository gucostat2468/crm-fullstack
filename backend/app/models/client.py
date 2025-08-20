from app import db
from app.models.note import Note
from app.models.task import Task

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Ativo')
    notes = db.relationship('Note', backref='client', lazy='dynamic', cascade="all, delete-orphan")
    tasks = db.relationship('Task', backref='client', lazy='dynamic', cascade="all, delete-orphan")