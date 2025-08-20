from app import ma, db
from app.models.note import Note
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class NoteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)