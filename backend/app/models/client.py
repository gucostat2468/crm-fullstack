from app import db
# --- ADIÇÕES IMPORTANTES AQUI ---
# Importamos os modelos explicitamente para que o SQLAlchemy possa encontrá-los
# ao construir os relacionamentos.
from app.models.note import Note
from app.models.task import Task
from app.models.file import File
# --------------------------------

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Ativo')
    
    # Agora o SQLAlchemy sabe o que 'Note', 'Task' e 'File' significam
    notes = db.relationship('Note', backref='client', lazy='dynamic', cascade="all, delete-orphan")
    tasks = db.relationship('Task', backref='client', lazy='dynamic', cascade="all, delete-orphan")
    files = db.relationship('File', backref='client', lazy='dynamic', cascade="all, delete-orphan")