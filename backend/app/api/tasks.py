from flask import Blueprint, jsonify, request
from app import db
from app.models.task import Task
from app.models.client import Client
from flask_login import login_required
from app.schemas.task_schema import task_schema, tasks_schema
from marshmallow import ValidationError

tasks_api = Blueprint('tasks_api', __name__)

@tasks_api.route('/clients/<int:client_id>/tasks', methods=['POST'])
@login_required
def create_task_for_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()

    try:
        new_task = task_schema.load(data)
        new_task.client_id = client.id
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        "message": "Tarefa criada com sucesso!",
        "task": task_schema.dump(new_task)
    }), 201

@tasks_api.route('/clients/<int:client_id>/tasks', methods=['GET'])
@login_required
def get_tasks_for_client(client_id):
    client = Client.query.get_or_404(client_id)
    tasks = client.tasks.order_by(Task.created_date.desc()).all()
    return jsonify(tasks_schema.dump(tasks))

@tasks_api.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    try:
        updated_task = task_schema.load(data, instance=task, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return jsonify({
        "message": "Tarefa atualizada com sucesso!",
        "task": task_schema.dump(updated_task)
    })

@tasks_api.route('/tasks/<int:task_id>/complete', methods=['PUT'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'Concluída'
    db.session.commit()
    return jsonify({"message": f"Tarefa '{task.title}' marcada como concluída!"})

@tasks_api.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa deletada com sucesso!"})