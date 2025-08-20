from flask import Blueprint, jsonify, request
from app import db
from app.models.client import Client
from flask_login import login_required
from app.schemas.client_schema import client_schema, clients_schema
from marshmallow import ValidationError

clients_api = Blueprint('clients_api', __name__)

@clients_api.route('/clients', methods=['GET'])
@login_required
def get_clients():
    search_term = request.args.get('search')
    status_filter = request.args.get('status')
    query = Client.query
    if search_term:
        query = query.filter(Client.name.ilike(f'%{search_term}%'))
    if status_filter:
        query = query.filter(Client.status == status_filter)
    clients_list = query.order_by(Client.name).all()
    return jsonify(clients_schema.dump(clients_list))

@clients_api.route('/clients/<int:client_id>', methods=['GET'])
@login_required
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client_schema.dump(client))

@clients_api.route('/clients', methods=['POST'])
@login_required
def create_client():
    data = request.get_json()
    try:
        new_client = client_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(new_client)
    db.session.commit()
    return jsonify({
        "message": "Cliente criado com sucesso!",
        "client": client_schema.dump(new_client)
    }), 201

@clients_api.route('/clients/<int:client_id>', methods=['PUT'])
@login_required
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    try:
        updated_client = client_schema.load(data, instance=client, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.commit()
    return jsonify({
        "message": "Cliente atualizado com sucesso!",
        "client": client_schema.dump(updated_client)
    })

@clients_api.route('/clients/<int:client_id>', methods=['DELETE'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Cliente deletado com sucesso!"})