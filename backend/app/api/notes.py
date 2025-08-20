from flask import Blueprint, jsonify, request
from app import db
from app.models.note import Note
from app.models.client import Client
from flask_login import login_required
from app.schemas.note_schema import note_schema, notes_schema
from marshmallow import ValidationError

notes_api = Blueprint('notes_api', __name__)

@notes_api.route('/clients/<int:client_id>/notes', methods=['POST'])
@login_required
def add_note_to_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    
    try:
        new_note = note_schema.load(data)
        new_note.client_id = client.id
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "message": "Nota adicionada com sucesso!",
        "note": note_schema.dump(new_note)
    }), 201

@notes_api.route('/clients/<int:client_id>/notes', methods=['GET'])
@login_required
def get_notes_for_client(client_id):
    client = Client.query.get_or_404(client_id)
    notes = client.notes.order_by(Note.created_date.desc()).all()
    return jsonify(notes_schema.dump(notes))

@notes_api.route('/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()

    try:
        updated_note = note_schema.load(data, instance=note, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify({
        "message": "Nota atualizada com sucesso!",
        "note": note_schema.dump(updated_note)
    })

@notes_api.route('/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Nota deletada com sucesso!"})